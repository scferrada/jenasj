package org.apache.jena.sparql.engine.join;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.jena.atlas.lib.PairOfSameType;
import org.apache.jena.datatypes.xsd.XSDDatatype;
import org.apache.jena.graph.Node;
import org.apache.jena.graph.NodeFactory;
import org.apache.jena.sparql.expr.Expr;
import org.apache.jena.sparql.expr.ExprList;

import com.eatthepath.jvptree.DistanceFunction;

import flann.metric.Metric;

public class Distances {
	
	private static Map<String, DistFunc> registry = new HashMap<String, Distances.DistFunc>();
	static {
		registry.put("manhattan", new DistFunc() {
			
			@Override
			public double distance(List<Node> p1, List<Node> p2, Map<Expr, PairOfSameType<Number>> minMax, ExprList leftExpr, ExprList rightExpr) {
				double d = 0.0;
				for (int i = 0; i < p1.size(); i++) {
					Node n1 = p1.get(i);
					Node n2 = p2.get(i);
					double maxX = minMax.get(leftExpr.get(i)).getRight().doubleValue();
					double minX = minMax.get(leftExpr.get(i)).getLeft().doubleValue();
					double x = (((Number) n1.getLiteralValue()).doubleValue() - minX)/(maxX-minX);
					double y = (((Number) n2.getLiteralValue()).doubleValue() - minX)/(maxX-minX);
					d += Math.abs(x - y);
				}
				return d;
			}
		});
		registry.put("euclidean", new DistFunc() {
			
			@Override
			public double distance(List<Node> p1, List<Node> p2, Map<Expr, PairOfSameType<Number>> minMax, ExprList leftExpr, ExprList rightExpr) {
				double d = 0;
				for (int i = 0; i < p1.size(); i++) {
					Node n1 = p1.get(i);
					Node n2 = p2.get(i);
					double maxX = minMax.get(leftExpr.get(i)).getRight().doubleValue();
					double minX = minMax.get(leftExpr.get(i)).getLeft().doubleValue();
					double x = (((Number) n1.getLiteralValue()).doubleValue() - minX)/(maxX-minX);
					double y = (((Number) n2.getLiteralValue()).doubleValue() - minX)/(maxX-minX);
					
					d += (x-y)*(x-y);
				}
				return d;
			}
		});
	}

	public interface DistFunc {
		public double distance(List<Node> p1, List<Node> p2, Map<Expr, PairOfSameType<Number>> minMax, ExprList leftExpr, ExprList rightExpr);
	}
	
	public static DistFunc getDistance(String distance) {
		return registry.get(distance.toLowerCase());
	}

	public static DistanceFunction<List<Double>> asVPFunction(DistFunc distFunc, Map<Expr, PairOfSameType<Number>> minMax, ExprList leftExpr, ExprList rightExpr) {
		DistanceFunction<List<Double>> res = new DistanceFunction<List<Double>>() {

			@Override
			public double getDistance(List<Double> firstPoint, List<Double> secondPoint) {
				List<Node> p1 = new ArrayList<Node>();
				List<Node> p2 = new ArrayList<Node>();
				for (int i = 0; i < firstPoint.size(); i++) {
					p1.add(NodeFactory.createLiteralByValue(firstPoint.get(i), XSDDatatype.XSDdouble));
					p2.add(NodeFactory.createLiteralByValue(secondPoint.get(i), XSDDatatype.XSDdouble));
				}
				return distFunc.distance(p1, p2, minMax, leftExpr, rightExpr);
			}
		};
		return res;
	}

	public static Metric getMetric(DistFunc distFunc, Map<Expr,PairOfSameType<Number>> minMax, ExprList leftExpr, ExprList rightExpr) {
		return new Metric() {
			
			List<Node> p1 = new ArrayList<Node>();
			List<Node> p2 = new ArrayList<Node>();
			
			@Override
			public int distance(int a, int b) {
				p1.add(NodeFactory.createLiteralByValue(a, XSDDatatype.XSDdouble));
				p2.add(NodeFactory.createLiteralByValue(b, XSDDatatype.XSDdouble));
				return (int) distFunc.distance(p1, p2, minMax, leftExpr, rightExpr);
			}
			
			@Override
			public int distance(int[] a, int[] b) {
				for (int i = 0; i < a.length; i++) {
					p1.add(NodeFactory.createLiteralByValue(a[i], XSDDatatype.XSDdouble));
					p2.add(NodeFactory.createLiteralByValue(b[i], XSDDatatype.XSDdouble));
				}
				return (int) distFunc.distance(p1, p2, minMax, leftExpr, rightExpr);
			}
			
			@Override
			public double distance(double a, double b) {
				p1.add(NodeFactory.createLiteralByValue(a, XSDDatatype.XSDdouble));
				p2.add(NodeFactory.createLiteralByValue(b, XSDDatatype.XSDdouble));
				return distFunc.distance(p1, p2, minMax, leftExpr, rightExpr);
			}
			
			@Override
			public double distance(double[] a, double[] b) {
				for (int i = 0; i < a.length; i++) {
					p1.add(NodeFactory.createLiteralByValue(a[i], XSDDatatype.XSDdouble));
					p2.add(NodeFactory.createLiteralByValue(b[i], XSDDatatype.XSDdouble));
				}
				return distFunc.distance(p1, p2, minMax, leftExpr, rightExpr);
			}
		};
	}

}
