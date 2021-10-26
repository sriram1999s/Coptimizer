// sort an array of positive integers
#include<stdio.h>
#include<stdbool.h>

void swap(int *xp, int *yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void sortArray(int *arr, int n)
{
    /*sort-positive-begin*/
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
    /*sort-positive-end*/
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
    // int arr[] = {2, 1, 3, 3, 2, 3};
    int arr[] = {37, 235, 908, 72, 767, 905, 645, 847, 960, 129, 972, 583, 749, 390, 281, 178, 276, 254, 357, 914, 468, 907, 252, 490, 925, 398, 562, 580, 215, 983, 753, 503, 478, 86, 141, 393, 7, 319, 829, 534, 313, 513, 896, 316, 209, 264, 728, 653, 627, 431, 633, 456, 71, 387, 917, 561, 313, 515, 964, 497, 588, 26, 820, 336, 621, 883, 297, 466, 15, 64, 196, 25, 367, 471, 903, 282, 616, 22, 777, 707, 999, 126, 381, 356, 155, 933, 313, 595, 166, 648, 288, 418, 778, 279, 655, 87, 793, 967, 243, 348, 586, 190, 302, 728, 151, 695, 321, 369, 845, 771, 896, 253, 461, 774, 564, 469, 514, 588, 987, 149, 715, 263, 77, 712, 75, 332, 43, 532, 548, 871, 775, 813, 964, 569, 752, 508, 210, 269, 10, 279, 892, 849, 903, 889, 152, 714, 476, 660, 416, 140, 193, 606, 572, 489, 152, 338, 883, 865, 130, 492, 615, 866, 266, 694, 864, 489, 850, 470, 198, 706, 327, 999, 176, 566, 15, 901, 401, 170, 20, 630, 944, 278, 485, 909, 609, 693, 852, 10, 183, 317, 568, 729, 405, 231, 505, 979, 25, 497, 910, 141, 212, 628, 811, 646, 717, 696, 955, 911, 536, 137, 450, 199, 821, 325, 420, 869, 760, 21, 296, 77, 219, 689, 369, 303, 461, 424, 462, 557, 855, 656, 924, 234, 557, 451, 884, 322, 974, 302, 384, 413, 63, 843, 547, 949, 477, 545, 642, 468, 595, 48, 822, 288, 253, 668, 55, 722, 287, 28, 222, 330, 136, 109, 611, 32, 520, 596, 973, 562, 591, 169, 832, 620, 211, 24, 113, 788, 44, 271, 670, 475, 910, 499, 787, 251, 666, 235, 86, 391, 739, 53, 431, 878, 444, 755, 290, 100, 740, 800, 915, 451, 792, 723, 229, 606, 166, 687, 231, 901, 79, 575, 881, 87, 416, 810, 714, 706, 728, 738, 670, 657, 324, 832, 188, 500, 206, 145, 167, 163, 465, 668, 662, 806, 681, 458, 717, 326, 665, 240, 48, 690, 958, 300, 617, 182, 256, 342, 503, 784, 275, 777, 624, 732, 51, 879, 138, 123, 324, 407, 270, 703, 533, 174, 380, 131, 440, 856, 208, 942, 566, 975, 583, 508, 526, 717, 143, 409, 821, 724, 505, 954, 981, 626, 750, 925, 556, 37, 150, 475, 438, 332, 524, 376, 315, 922, 972, 967, 727, 423, 637, 43, 460, 882, 806, 603, 624, 253, 837, 738, 417, 171, 410, 696, 965, 585, 308, 601, 539, 43, 1, 338, 127, 606, 992, 410, 852, 542, 871, 64, 150, 610, 820, 643, 70, 652, 295, 230, 83, 751, 176, 317, 454, 781, 164, 279, 406, 450, 634, 476, 249, 490, 351, 565, 905, 681, 441, 856, 365, 758, 733, 756, 716, 850, 362, 907, 105, 36, 112, 144, 158, 115, 618, 212, 953, 803, 425, 337, 770, 213, 93, 164, 621, 302, 848, 795, 328, 540, 642, 739, 397, 425, 889, 292, 740, 168, 18, 225, 934, 319, 499, 558, 360, 217, 999, 112, 511, 357, 514, 98, 796, 718, 715, 442, 682, 794, 232, 917, 570, 895, 400, 988, 549, 237, 488, 234, 779, 918, 518, 96, 654, 100, 343, 203, 931, 703, 379, 544, 622, 859, 689, 998, 890, 128, 662, 97, 454, 676, 914, 795, 668, 485, 564, 614, 498, 734, 377, 818, 814, 519, 469, 272, 743, 669, 907, 445, 782, 360, 542, 136, 168, 944, 158, 407, 450, 732, 704, 743, 140, 657, 762, 417, 522, 28, 971, 901, 849, 645, 889, 42, 598, 948, 825, 312, 590, 855, 373, 721, 906, 712, 816, 501, 787, 396, 153, 333, 784, 260, 984, 886, 667, 946, 836, 643, 698, 524, 130, 844, 352, 864, 317, 399, 356, 506, 842, 908, 914, 158, 955, 645, 144, 863, 608, 956, 427, 748, 287, 747, 611, 300, 792, 958, 847, 533, 915, 845, 545, 4, 551, 124, 67, 162, 162, 42, 846, 722, 870, 38, 378, 688, 122, 721, 510, 773, 506, 230, 219, 501, 392, 296, 197, 517, 7, 462, 805, 873, 334, 545, 539, 691, 77, 30, 939, 174, 9, 835, 771, 963, 822, 353, 959, 227, 592, 284, 677, 448, 421, 989, 402, 334, 359, 454, 988, 52, 394, 814, 63, 635, 733, 658, 932, 157, 504, 39, 796, 566, 29, 183, 359, 346, 923, 956, 874, 396, 145, 71, 603, 903, 380, 467, 184, 563, 716, 574, 102, 179, 608, 542, 150, 261, 475, 95, 361, 406, 716, 116, 365, 22, 998, 402, 221, 285, 18, 52, 122, 543, 305, 738, 467, 377, 733, 173, 747, 947, 342, 783, 199, 688, 412, 723, 795, 811, 147, 591, 838, 344, 214, 523, 229, 449, 605, 271, 691, 994, 854, 557, 371, 447, 938, 662, 109, 615, 466, 168, 684, 912, 273, 875, 600, 230, 896, 240, 353, 82, 887, 967, 500, 14, 676, 26, 928, 897, 944, 344, 501, 22, 802, 862, 533, 196, 963, 688, 118, 146, 353, 651, 651, 377, 436, 844, 580, 173, 192, 89, 552, 775, 775, 246, 289, 570, 263, 162, 132, 389, 957, 118, 871, 178, 588, 429, 254, 352, 917, 114, 381, 92, 327, 732, 751, 665, 489, 247, 865, 1, 269, 116, 38, 213, 411, 678, 980, 161, 769, 415, 245, 113, 626, 294, 28, 715, 626, 867, 31, 179, 66, 835, 928, 842, 928, 993, 773, 0, 933, 366, 840, 427, 364, 792, 144, 381, 864, 224, 297, 152, 277, 923, 46, 291, 318, 68, 318, 893, 544, 249, 45, 856, 358, 371, 938, 57, 665, 800, 360, 33, 502, 646, 193, 307, 543, 391, 251, 141, 127, 387, 412, 655, 797, 578, 751, 61, 723, 96, 570, 978, 744, 506, 930, 798, 185, 96, 945, 508, 814, 339, 809, 276, 504, 40, 888, 510, 110, 434, 502, 132, 265, 124, 384, 218, 405, 507, 74, 149, 246, 417, 887, 166, 805, 555};
    int n = sizeof(arr)/sizeof(int);
    sortArray(arr, n);
    display(arr, n);
    return 0;
}