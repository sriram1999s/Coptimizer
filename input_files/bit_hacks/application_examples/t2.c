// sort an array of unique positive integers
#include<stdio.h>
#include<stdbool.h>

void swap(int *xp, int *yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void sortUniquePositiveIntegers(int *arr, int n)
{
    /*sort-unique-positive-begin*/
    /*(arr,n)*/
    int i, j;
   bool swapped;
   for (i = 0; i < n-1; i++)
   {
     swapped = false;
     for (j = 0; j < n-i-1; j++)
     {
        if (arr[j] > arr[j+1])
        {
           swap(&arr[j], &arr[j+1]);
           swapped = true;
        }
     }

     // IF no two elements were swapped by inner loop, then break
     if (swapped == false)
        break;
   }
    /*sort-unique-positive-end*/
}

void display(int* arr, int n)
{
    for(int i=0; i<n; ++i)
    {
        printf("%d ", arr[i]);
    }
}

int main()
{
//    int arr[] = {3, 6, 1, 2, 7, 9, 5, 8, 0, 4};
    int arr[] = {2222, 127, 1794, 1749, 1578, 512, 1590, 163, 1200, 1587, 3776, 3564, 1461, 576, 345, 1599, 1717, 3725, 630, 2669, 1510, 3254, 2101, 2979, 3242, 916, 2748, 2689, 568, 1844, 199, 251, 2132, 1728, 3891, 2261, 3386, 3971, 1002, 1401, 214, 3047, 284, 2606, 3561, 1736, 1308, 1931, 1881, 3620, 3002, 2945, 182, 2726, 1991, 3827, 2928, 2119, 904, 3381, 3482, 171, 2860, 729, 403, 3123, 1925, 1778, 3989, 1397, 867, 3232, 2664, 3642, 366, 1521, 2601, 53, 2442, 2946, 2423, 1880, 1636, 1116, 991, 1614, 2485, 423, 897, 1364, 2649, 424, 3872, 3864, 3684, 3623, 3641, 3532, 2833, 1524, 3015, 1387, 333, 3960, 1261, 1295, 2559, 2241, 2632, 453, 883, 3059, 3036, 3437, 1332, 3413, 1808, 828, 2035, 599, 2911, 532, 3700, 494, 3203, 3987, 486, 1250, 3125, 3353, 1212, 3903, 3908, 3432, 3029, 3753, 3800, 3095, 725, 3369, 2341, 1346, 2912, 768, 2830, 3818, 1446, 1238, 1076, 1373, 2293, 899, 2418, 2097, 2690, 3976, 620, 1807, 3235, 112, 2158, 337, 3943, 1405, 3114, 3418, 2903, 437, 3798, 3013, 2192, 780, 651, 3136, 1010, 685, 3166, 3017, 3216, 1088, 1669, 2555, 1336, 2468, 3339, 2539, 1888, 3612, 3023, 583, 794, 2073, 743, 3820, 714, 1901, 863, 728, 2530, 2175, 3633, 799, 2374, 447, 820, 1838, 1371, 1351, 2993, 68, 518, 1709, 1792, 477, 751, 2648, 3574, 3645, 2447, 3069, 2952, 1990, 2497, 3207, 2187, 448, 1603, 2209, 390, 917, 1882, 2518, 801, 2466, 1251, 3838, 650, 1851, 1004, 2364, 2623, 972, 432, 1708, 3650, 3470, 3969, 1460, 2456, 856, 2531, 710, 2605, 693, 3414, 3171, 2750, 1508, 2923, 2560, 3516, 3140, 542, 167, 2688, 2243, 2040, 3399, 2811, 3811, 348, 3892, 3955, 3425, 730, 3786, 3359, 3785, 1203, 1333, 2169, 394, 1737, 2494, 3448, 3179, 2888, 1522, 2506, 2324, 2432, 3070, 1790, 1008, 452, 1215, 2171, 6, 2999, 3590, 1660, 3134, 1164, 2450, 1678, 3149, 2589, 2743, 877, 2342, 1290, 1272, 2885, 925, 1961, 800, 1964, 56, 3951, 747, 3787, 3738, 2372, 1891, 1638, 1774, 1820, 2803, 445, 483, 2528, 3119, 2515, 2352, 2407, 921, 469, 1616, 872, 1012, 632, 114, 964, 3988, 1471, 642, 1181, 1486, 2965, 3274, 1505, 3599, 655, 3841, 1462, 1932, 2391, 2529, 2858, 3992, 2075, 1559, 2287, 2268, 2459, 2603, 414, 1056, 2988, 1474, 307, 502, 3040, 1694, 3870, 1385, 536, 2321, 1533, 2639, 2104, 782, 3223, 1542, 739, 588, 2509, 574, 2260, 624, 1747, 2465, 1623, 443, 2625, 3401, 1543, 3099, 984, 2085, 2617, 3234, 2109, 3711, 874, 2954, 3539, 3900, 1488, 2048, 1500, 3342, 1363, 3587, 3610, 998, 3499, 1519, 1123, 3777, 3529, 1170, 200, 3026, 1609, 3913, 833, 1610, 2602, 906, 1274, 1959, 62, 524, 1780, 1223, 1885, 1375, 144, 1036, 2153, 815, 763, 495, 888, 1383, 1752, 2477, 381, 222, 1344, 455, 292, 1281, 3186, 1331, 671, 245, 3927, 1525, 470, 3345, 3169, 2766, 172, 1309, 3984, 3589, 2280, 1870, 3613, 35, 992, 1166, 2139, 3849, 1359, 3438, 2760, 173, 3237, 1098, 3402, 2751, 1418, 2393, 1063, 2753, 930, 1141, 1395, 410, 3423, 886, 623, 704, 756, 2228, 2814, 3975, 1741, 1748, 2950, 196, 3832, 3565, 619, 2353, 1803, 2121, 1517, 3071, 1496, 1182, 396, 2796, 919, 2898, 2544, 1064, 2729, 1656, 1252, 3037, 849, 852, 864, 1356, 2569, 1253, 3198, 3675, 1191, 2739, 2350, 3666, 2062, 1022, 1222, 3826, 2740, 2472, 3813, 3560, 1353, 506, 2326, 2229, 1854, 2051, 209, 3533, 2608, 3545, 2148, 1075, 1967, 3244, 501, 1003, 3340, 1384, 2977, 3509, 58, 2595, 1915, 933, 3208, 660, 688, 1974, 737, 1323, 1630, 2523, 3067, 3720, 26, 3318, 1449, 1960, 85, 242, 1850, 3249, 86, 2258, 268, 3609, 2644, 557, 1833, 3993, 1132, 183, 2549, 3479, 593, 2002, 773, 3016, 3260, 1032, 513, 845, 1949, 1715, 3834, 478, 1477, 3012, 3100, 1650, 2869, 2336, 638, 3411, 1547, 3866, 2474, 1208, 2242, 3801, 2001, 721, 162, 3382, 3072, 3127, 2320, 142, 3876, 3859, 2351, 1712, 3559, 2050, 3719, 258, 50, 476, 1118, 1206, 3210, 2827, 2032, 421, 3747, 3562, 673, 1563, 134, 2098, 1121, 42, 1911, 1146, 120, 327, 1389, 1390, 343, 970, 1913, 334, 2256, 3227, 2687, 55, 2504, 1598, 3660, 2800, 2215, 1569, 1006, 3074, 2955, 2581, 1937, 1224, 1199, 3419, 425, 2369, 967, 181, 2924, 3344, 1779, 269, 3000, 2142, 3930, 3520, 2055, 1120, 866, 2413, 2773, 533, 541, 2854, 1168, 635, 1402, 3780, 2052, 3647, 376, 3794, 3506, 3737, 1330, 2309, 1136, 2446, 3019, 3656, 500, 2794, 1982, 2686, 1594, 2173, 956, 699, 2231, 225, 3226, 2249, 111, 1837, 3096, 1727, 789, 2951, 2553, 2807, 3898, 1403, 3704, 1996, 1455, 3159, 3584, 590, 646, 2416, 986, 2694, 3924, 94, 960, 2383, 2967, 3421, 3284, 1822, 2682, 208, 2179, 3450, 310, 1430, 1642, 3762, 708, 1771, 1451, 3758, 3831, 3804, 1734, 678, 2106, 772, 1023, 1044, 41, 201, 1687, 3396, 2983, 2129, 2305, 417, 1404, 316, 2984, 796, 1205, 2974, 1567, 2655, 1447, 1276, 3963, 160, 2160, 1968, 1899, 1103, 2373, 3544, 2056, 1992, 610, 1038, 2835, 1829, 2764, 31, 57, 3206, 3578, 2227, 3998, 2130, 1903, 3137, 3471, 1193, 1724, 267, 567, 3848, 2275, 130, 929, 1245, 370, 1350, 2917, 1576, 3441, 645, 2598, 2464, 2274, 1649, 1515, 3407, 23, 1597, 1827, 465, 1478, 974, 2105, 126, 1171, 3879, 2940, 3272, 3046, 2213, 2246, 2402, 3103, 3385, 2651, 2943, 2100, 2247, 3591, 2557, 2791, 3503, 3264, 2108, 59, 1456, 3626, 1111, 413, 3688, 1689, 947, 1681, 2502, 672, 2735, 3161, 2408, 2500, 2727, 1291, 937, 419, 764, 965, 351, 2809, 3923, 1230, 227, 1506, 2828, 2561, 207, 1676, 30, 3850, 2942, 2749, 1933, 979, 3004, 116, 3904, 33, 3422, 2277, 1799, 1495, 2492, 3741, 2960, 2975, 3243, 3654, 571, 3607, 3356, 107, 659, 1113, 1700, 3162, 781, 621, 766, 2711, 3080, 436, 3195, 1195, 13, 3677, 3844, 3604, 3280, 1324, 2155, 2003, 3696, 900, 2558, 885, 2805, 612, 3304, 2793, 3048, 1690, 155, 2668, 1632, 3933, 1965, 3218, 3679, 775, 784, 2730, 2626, 358, 3937, 262, 3982, 3485, 1020, 1233, 3371, 1551, 498, 165, 3077, 825, 953, 3515, 752, 566, 3885, 1320, 3994, 3603, 686, 3148, 792, 2489, 1013, 854, 2401, 1374, 346, 1878, 2024};
    int n = sizeof(arr)/sizeof(int);
    sortUniquePositiveIntegers(arr, n);
    display(arr, n);
    return 0;
}