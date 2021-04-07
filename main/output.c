int foo()
{
    return 1;
}

float bar()
{
    int b1 = 2.5;
    return b1;
}

double goo()
{
    int g1 = 3.908176267818;
    return g1;
}

int main()
{
    int res_foo;
    int temp_6a2b0abb0d174e89bcafbdc5ed9951ab;
    {				// foo inlined 
	temp_6a2b0abb0d174e89bcafbdc5ed9951ab = 1;
    }

    res_foo = temp_6a2b0abb0d174e89bcafbdc5ed9951ab;
    int res_bar;
    int temp_5165f1b60bd045f28cb7df1293f4e86c;
    {				// bar inlined 
	int b1 = 2.5;
	temp_5165f1b60bd045f28cb7df1293f4e86c = b1;
    }

    res_bar = temp_5165f1b60bd045f28cb7df1293f4e86c;
    double res_goo;
    double temp_5dca040a23474d7c8aca0177064ef236;
    {				// goo inlined 
	int g1 = 3.908176267818;
	temp_5dca040a23474d7c8aca0177064ef236 = g1;
    }

    res_goo = temp_5dca040a23474d7c8aca0177064ef236;
    return 0;
}
