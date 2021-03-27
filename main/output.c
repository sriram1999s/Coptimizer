void foo(int f)
{
	f = 1;
} int bar(int b1, int b2)
{
	int b = b1 + b2;
	return b;
}

float goo(int g1, float g2, float g3)
{
	float prod = g2 * g3;
	float sum = prod + g1;
	return sum;
}

int main()
{
	int g11 = 10;
	float g22 = 0.5;
	float g33 = 1.0; {	// foo inlined 
		int f_48d4595385f342e2b5647a750759bdb5 =
		    g22 / ((g22 + g33) * g33);
		f_48d4595385f342e2b5647a750759bdb5 = 1;
	}
	;
	int res_bar;
	int temp_f746598d825e46899f6fa5e06a13902f;
	{			// bar inlined 
		int b1_f746598d825e46899f6fa5e06a13902f = 1;
		int b2_f746598d825e46899f6fa5e06a13902f = 2;
		int b =
		    b1_f746598d825e46899f6fa5e06a13902f +
		    b2_f746598d825e46899f6fa5e06a13902f;
		temp_f746598d825e46899f6fa5e06a13902f = b;
	}

	res_bar = temp_f746598d825e46899f6fa5e06a13902f;
	float res_goo;
	float temp_a4bda8479e7b45439d9043ed5ba996d6;
	{			// goo inlined 
		int g1_a4bda8479e7b45439d9043ed5ba996d6 = g11;
		float g2_a4bda8479e7b45439d9043ed5ba996d6 = g22 + g33;
		float g3_a4bda8479e7b45439d9043ed5ba996d6 = g33;
		float prod =
		    g2_a4bda8479e7b45439d9043ed5ba996d6 *
		    g3_a4bda8479e7b45439d9043ed5ba996d6;
		float sum = prod + g1_a4bda8479e7b45439d9043ed5ba996d6;
		temp_a4bda8479e7b45439d9043ed5ba996d6 = sum;
	}

	res_goo = temp_a4bda8479e7b45439d9043ed5ba996d6;
	return 0;
}
