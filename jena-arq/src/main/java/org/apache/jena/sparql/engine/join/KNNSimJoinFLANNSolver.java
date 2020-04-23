package org.apache.jena.sparql.engine.join;

import java.util.LinkedList;
import java.util.List;

import org.apache.jena.sparql.engine.binding.Binding;
import org.apache.jena.sparql.engine.join.QueryIterSimJoin.Neighbor;
import org.apache.jena.sparql.expr.Expr;

import flann.index.IndexKDTree;
import flann.index.IndexKDTree.SearchParams;
import flann.metric.Metric;

public class KNNSimJoinFLANNSolver extends KNNSimJoinSolver {

	double[][] data;
	private List<Binding> rightRows;
	private SearchParams searchParams2;
	private IndexKDTree index;
	
	public KNNSimJoinFLANNSolver(QueryIterSimJoin simjoin) {
		super(simjoin);
		this.rightRows = simjoin.getRightRows();
		this.bindingIterator = this.rightRows.iterator();
	}

	@Override
	public void setUp() {
		materialise();
		QueryIterKNNSimJoin knnsimjoin = (QueryIterKNNSimJoin) simjoin;
		Metric metric = Distances.getMetric(knnsimjoin.distFunc, knnsimjoin.minMax, knnsimjoin.leftAttributes, knnsimjoin.rightAttributes);
        IndexKDTree.BuildParams buildParams = new IndexKDTree.BuildParams(4);
        index = new IndexKDTree(metric, data, buildParams);
        index.buildIndex();
        searchParams2 = new IndexKDTree.SearchParams();
        searchParams2.eps = 0.0f;
        searchParams2.maxNeighbors = knnsimjoin.getK()+1;
        searchParams2.checks = 128;
	}

	private void materialise() {
		List<List<Double>> res = new LinkedList<>();
        for(;bindingIterator.hasNext();){
        	Binding b = bindingIterator.next();
            List<Double> row = new LinkedList<>();
            for (Expr v : simjoin.rightAttributes ) {
                row.add(((Number)b.get(v.asVar()).getLiteralValue()).doubleValue());
            }
            res.add(row);
        }
        data = res.stream().map(l->l.stream().mapToDouble(Double::doubleValue).toArray()).toArray(double[][]::new);
	}

	@Override
	protected void getNextBatch(Binding l) {
		QueryIterKNNSimJoin knnsimjoin = (QueryIterKNNSimJoin) simjoin;
        int[][] indices = new int[1][knnsimjoin.getK()+1];
        double[][] distances = new double[1][knnsimjoin.getK()+1];
            List<Double> lvals = new LinkedList<>();
            for (Expr v : knnsimjoin.getLeftAttributes().getListRaw()) {
                lvals.add(((Number)l.get(v.asVar()).getLiteralValue()).doubleValue());
            }
            double[][] query = new double[1][lvals.size()];
            query[0] = lvals.stream().mapToDouble(Double::doubleValue).toArray();
            index.knnSearch(query, indices, distances, searchParams2);
            for(int j=1; j<=knnsimjoin.getK(); j++){
                cache.add(new Neighbor<>(rightRows.get(indices[0][j]), distances[0][j]));
            }       
	}
}
