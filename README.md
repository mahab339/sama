# sama
Engineering Economic Analysis - Calculator Interpreter.

Sama is an interpreter for discrete compounding formulas with discrete payments.

A simple user interface (in www folder) is hosted at http://sama.elasticbeanstalk.com/

You can calculate long calculations at once, for example: <br>(20000(P|A, 15%, 2) + 25000(P|A, 0.15, 3)(P|F, 15%, 2)) * (A|P, 15%, 5) = 22575.128779613286

Supported formulas and syntax:
* (F|P, i, n)
* (P|F, i, n)
* (F|A, i, n)
* (A|F, i, n)
* (P|A, i, n)
* (A|P, i, n)
* (P|G, i, N)
* (A|G, i, N)
* (P|A1, g, i, N)


## TODO
* Enhance the website frontend.
* Add history feature, for previously inserted calculations.
