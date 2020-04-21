package org.apache.jena.sparql.algebra.op;

import org.apache.jena.sparql.algebra.Op;
import org.apache.jena.sparql.engine.ExecutionContext;
import org.apache.jena.sparql.engine.QueryIterator;
import org.apache.jena.sparql.engine.join.QueryIterRangeSimJoin;
import org.apache.jena.sparql.engine.join.QueryIterSimJoin;
import org.apache.jena.sparql.expr.ExprList;
import org.apache.jena.sparql.sse.Tags;

public class OpRangeSimJoin extends OpSimJoin implements Op {

	private double within;

	public OpRangeSimJoin(Op left, Op right, double within, String distance, ExprList leftAttrs, ExprList rightAttrs) {
		super(left, right, distance, leftAttrs, rightAttrs);
		this.within = within;
	}

	@Override
	public int getTop() {
		return -1;
	}

	@Override
	public double getWithin() {
		return within;
	}

	@Override
	public String getName() {
		return (Tags.tagRangeSimJoin) + " ("+within+")";
	}

	@Override
	public Op2 copy(Op left, Op right) {
		return new OpRangeSimJoin(left, right, within, distance, leftAttributes, rightAttributes);
	}

	@Override
	public QueryIterator createIterator(QueryIterator left, QueryIterator right, ExecutionContext execCxt) {
		// TODO Auto-generated method stub
		return QueryIterRangeSimJoin.createRange(left, right, this, execCxt);
	}

}
