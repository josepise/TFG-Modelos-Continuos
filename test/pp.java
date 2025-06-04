import java.util.*;
import java.io.*;

public class pp{ 
	public static final int n_equations = 4;

	public static double tol = 1e-6; // Tolerance for RKF45
	// Model parameters
	public static double a = 2.0;

	public static double t0 = 0;
	public static double tf = 50;
	public static double dt = 0.1;
	public static List<Double> t = new ArrayList<>(Arrays.asList(t0));

	public static List<List<Double>> est = new ArrayList<>(n_equations);

	static class Pair<T, U> {
		private T first;
		private U second;

		public Pair(T first, U second) {
			this.first = first;
			this.second = second;
		}

		public T getKey() {
			return first;
		}

		public U getValue() {
			return second;
		}

	}

	public static List<Double> deriv(List<Double> inp) {
		// Conditions
		Double p_1=a*inp.get(2) - inp.get(0)*inp.get(1) - inp.get(0);
		Double p_2=inp.get(0) - inp.get(1)*inp.get(3) - inp.get(1);
		Double p_3=inp.get(1) - inp.get(2)*inp.get(3) - inp.get(3);
		Double p_4=-inp.get(2) + inp.get(3);
		return Arrays.asList(p_1, p_2, p_4, p_3);
	}

	public static Pair<List<Double>, Double> rkf45Step(double hh, List<Double> inp) {
		double[] a = {0, 1.0 / 4, 3.0 / 8, 12.0 / 13, 1.0, 1.0 / 2};
		double[][] b = {
			{0, 0, 0, 0, 0},
			{1.0 / 4, 0, 0, 0, 0},
			{3.0 / 32, 9.0 / 32, 0, 0, 0},
			{1932.0 / 2197, -7200.0 / 2197, 7296.0 / 2197, 0, 0},
			{439.0 / 216, -8, 3680.0 / 513, -845.0 / 4104, 0},
			{-8.0 / 27, 2, -3544.0 / 2565, 1859.0 / 4104, -11.0 / 40}
		};
		double[] c4 = {25.0 / 216, 0, 1408.0 / 2565, 2197.0 / 4104, -1.0 / 5, 0};
		double[] c5 = {16.0 / 135, 0, 6656.0 / 12825, 28561.0 / 56430, -9.0 / 50, 2.0 / 55};
		List<List<Double>> k = new ArrayList<>();
		for (int i = 0; i < 6; ++i) {
			List<Double> yTemp = new ArrayList<>(n_equations);
			for (int j = 0; j < n_equations; ++j) {
				double sum = 0;
				for (int m = 0; m < i; ++m) {
					sum += b[i][m] * k.get(m).get(j);
				}
				yTemp.add(i > 0 ? inp.get(j) + hh * sum : inp.get(j));
			}
			k.add(deriv(yTemp));
		}
		List<Double> y4 = new ArrayList<>(n_equations);
		List<Double> y5 = new ArrayList<>(n_equations);
		for (int j = 0; j < n_equations; ++j) {
			double sum4 = 0, sum5 = 0;
			for (int i = 0; i < 6; ++i) {
				sum4 += c4[i] * k.get(i).get(j);
				sum5 += c5[i] * k.get(i).get(j);
			}
			y4.add(inp.get(j) + hh * sum4);
			y5.add(inp.get(j) + hh * sum5);
		}
		double error = 0;
		for (int j = 0; j < n_equations; ++j) {
			error += Math.pow(y5.get(j) - y4.get(j), 2);
		}
		error = Math.sqrt(error);
		return new Pair<>(y5, error);
	}

	public static void main(String[] args) throws IOException {
		for (int i = 0; i < n_equations; ++i) {
			est.add(new ArrayList<>(Collections.singletonList(0.0)));
		}

		if (args.length < 8) {
			System.out.println("Error in the number of parameters: java " + 
				"pp" + " <a> <p_1> <p_2> <p_4> <p_3> <t_0> <t_f> <tol>");
			System.exit(1);
		}

		int numArgs = 0;

		a = Double.parseDouble(args[numArgs++]);
		est.get(0).set(0,Double.parseDouble(args[numArgs++])); // p_1
		est.get(1).set(0,Double.parseDouble(args[numArgs++])); // p_2
		est.get(2).set(0,Double.parseDouble(args[numArgs++])); // p_4
		est.get(3).set(0,Double.parseDouble(args[numArgs++])); // p_3
		t0 = Double.parseDouble(args[numArgs++]);
		tf = Double.parseDouble(args[numArgs++]);
		tol = Double.parseDouble(args[numArgs++]);

		double h = dt;
		while (t.get(t.size() - 1) < tf) {
			List<Double> inp = new ArrayList<>(n_equations);
			List<Double> y_new = new ArrayList<>(n_equations);
			double error;

			for (int i = 0; i < n_equations; ++i) {
				inp.add(est.get(i).get(est.get(i).size() - 1));
			}

			Pair<List<Double>, Double> result = rkf45Step(h, inp);
			y_new = result.getKey();
			error = result.getValue();

			if (error <= tol) {
				t.add(t.get(t.size() - 1) + h);
				for (int i = 0; i < n_equations; ++i) {
					est.get(i).add(y_new.get(i));
				}
			}

			h *= Math.min(5.0, Math.max(0.2, 0.84 * Math.pow(tol / error, 0.25)));
			h = Math.min(h, tf - t.get(t.size() - 1));
		}
		// Save the results to a CSV file
		try (BufferedWriter results = new BufferedWriter(new FileWriter("pp_output_java.csv"))) {
			results.write("t");
			results.write("	 p_1");
			results.write("	 p_2");
			results.write("	 p_4");
			results.write("	 p_3");
			results.newLine();
			for (int i = 0; i < est.get(0).size(); ++i) {
				results.write(t.get(i).toString());
				for (int j = 0; j < n_equations; ++j) {
					results.write("\t" + est.get(j).get(i));
				}
				results.newLine();
			}
		}
	}
}
