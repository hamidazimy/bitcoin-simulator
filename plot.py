#/usr/bin/python3

import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

foo = np.array([
[   0.542,	0.491,	0.503,	0.502,	0.492,	0.51,	0.529,	0.515,	0.482,	0.474,	0.475,	0.457,	0.48,	0.48,	0.445,	0.446,	0.401,	0.408,	0.383,	0.391,	0.401,	0.454,	0.361,	0.363,	0.386,	0.396,	0.329,	0.381,	0.4,	0.32,	0.319,	0.301,	0.343,	0.258,	0.308,	0.283,	0.288,	0.274,	0.283,	0.282],
[   1.623,	1.449,	1.526,	1.423,	1.472,	1.487,	1.528,	1.457,	1.377,	1.324,	1.408,	1.283,	1.273,	1.246,	1.204,	1.19,	1.145,	1.108,	1.167,	1.145,	1.181,	1.041,	1.041,	1.09,	1.034,	0.999,	1.022,	0.948,	0.951,	0.946,	0.925,	0.888,	0.951,	0.859,	0.858,	0.84,	0.814,	0.792,	0.754,	0.747],
[   3.087,	3.03,	2.755,	2.786,	2.686,	2.774,	2.707,	2.741,	2.634,	2.597,	2.456,	2.462,	2.453,	2.406,	2.316,	2.293,	2.26,	2.424,	2.212,	2.095,	2.113,	2.103,	2.08,	1.965,	2.035,	1.851,	1.861,	1.81,	1.709,	1.753,	1.805,	1.676,	1.724,	1.561,	1.533,	1.453,	1.484,	1.332,	1.468,	1.333],
[   4.831,	4.745,	4.762,	4.572,	4.555,	4.585,	4.33,	4.362,	4.193,	4.312,	4.071,	4.019,	3.973,	3.902,	3.823,	3.789,	3.72,	3.648,	3.596,	3.384,	3.582,	3.391,	3.165,	3.206,	3.043,	3.073,	3.073,	3.015,	2.814,	2.838,	2.8,	2.687,	2.68,	2.633,	2.474,	2.474,	2.214,	2.336,	2.306,	2.295],
[   7.441,	7.117,	7.151,	6.588,	6.644,	6.687,	6.427,	6.397,	6.225,	6.102,	6.083,	6.077,	5.885,	5.855,	5.584,	5.433,	5.332,	5.147,	5.123,	5.108,	4.923,	4.934,	4.78,	4.732,	4.587,	4.446,	4.444,	4.379,	4.187,	4.282,	4.106,	3.963,	3.936,	3.868,	3.707,	3.536,	3.326,	3.452,	3.264,	3.25],
[   9.931,	9.634,	9.735,	9.577,	9.476,	9.064,	9.005,	8.738,	8.705,	8.547,	8.321,	8.112,	8.292,	7.835,	7.562,	7.343,	7.328,	7.437,	7.071,	7.169,	6.907,	6.656,	6.548,	6.412,	6.443,	6.088,	5.87,	5.743,	5.799,	5.647,	5.707,	5.463,	5.393,	5.011,	5.269,	4.774,	4.678,	4.803,	4.564,	4.194],
[   12.798,	12.674,	12.51,	12.332,	12.075,	11.723,	11.686,	11.308,	11.145,	10.878,	10.884,	10.665,	10.316,	10.073,	10.174,	9.951,	9.645,	9.698,	9.128,	9.217,	8.863,	8.588,	8.573,	8.411,	8.055,	8.002,	7.809,	7.822,	7.306,	7.209,	7.081,	6.73,	6.653,	6.646,	6.485,	6.305,	5.98,	5.857,	5.85,	5.65],
[   16.087,	15.935,	15.624,	15.542,	15.19,	14.579,	14.765,	14.574,	14.306,	13.876,	13.604,	13.389,	13.188,	12.983,	12.57,	12.554,	12.073,	11.765,	11.311,	11.09,	11.192,	10.704,	10.556,	10.245,	10.018,	9.793,	9.749,	9.56,	9.099,	8.825,	8.727,	8.443,	8.128,	7.768,	7.962,	7.735,	7.658,	7.551,	7.165,	7.055],
[   20.061,	19.585,	19.343,	18.784,	18.733,	18.143,	18.093,	17.406,	17.314,	16.729,	16.369,	15.811,	16.029,	15.44,	15.088,	14.591,	14.778,	14.084,	13.892,	13.589,	13.573,	12.989,	12.698,	12.56,	12.2,	11.886,	11.512,	11.372,	11.117,	10.825,	10.276,	9.964,	9.63,	9.78,	9.26,	8.982,	8.953,	8.441,	8.106,	8.075],
[   24.056,	23.23,	23.111,	22.46,	21.823,	21.237,	21.152,	20.389,	20.324,	20.073,	19.556,	19.069,	18.75,	18.258,	17.582,	17.146,	17.182,	16.661,	16.363,	15.836,	15.491,	14.923,	14.628,	14.315,	13.926,	13.445,	13.29,	12.763,	12.673,	12.218,	11.721,	11.659,	11.241,	10.763,	10.456,	9.966,	9.818,	9.473,	9.393,	8.957],
[   28.295,	27.268,	27.267,	26.072,	25.908,	25.363,	24.777,	24.382,	23.375,	23.165,	22.262,	21.581,	21.441,	20.563,	20.035,	19.833,	19.172,	19.119,	18.082,	18.004,	17.259,	16.835,	16.474,	15.769,	15.385,	14.827,	14.638,	13.845,	13.669,	13.051,	13.021,	11.854,	11.481,	11.26,	11.217,	10.712,	10.216,	9.738,	9.487,	8.86],
[   33.106,	32.307,	31.506,	29.911,	29.081,	28.443,	27.782,	26.938,	26.146,	25.481,	24.353,	24.084,	23.893,	22.748,	22.217,	20.903,	20.532,	20.517,	19.312,	18.721,	17.731,	17.347,	16.96,	16.351,	15.592,	15.068,	14.168,	13.557,	13.085,	12.78,	11.938,	11.573,	11.067,	10.584,	10.154,	9.899,	9.501,	8.972,	8.411,	8.258],
[   38.182,	36.648,	35.903,	34.201,	32.342,	31.462,	30.058,	28.397,	27.979,	26.729,	24.713,	24.542,	23.71,	22.551,	20.674,	20.63,	19.251,	18.248,	18.258,	16.758,	15.395,	15.193,	14.717,	14.199,	13.256,	13.171,	11.468,	10.898,	10.947,	10.309,	9.554,	9.044,	8.69,	8.119,	7.674,	7.512,	7.005,	6.172,	6.032,	5.637],
[   43.044,	40.963,	37.59,	34.781,	33.181,	31.283,	29.269,	26.267,	24.906,	23.758,	22.415,	20.008,	18.104,	18.19,	15.108,	15.33,	13.628,	14.188,	12.498,	11.364,	11.43,	10.287,	9.449,	9.742,	8.538,	7.764,	7.418,	7.146,	6.314,	6.183,	6.11,	5.651,	5.17,	4.677,	4.739,	4.463,	3.903,	3.779,	3.454,	3.119],
[   47.154,	44.585,	37.443,	36.213,	32.267,	29.561,	24.982,	22.784,	21.195,	17.475,	16.452,	14.203,	13.07,	11.701,	10.065,	8.972,	8.233,	7.038,	7.553,	6.48,	6.088,	5.632,	5.153,	4.613,	4.55,	4.401,	4.37,	3.994,	3.444,	3.478,	2.901,	2.842,	2.764,	2.736,	2.674,	2.206,	1.97,	1.793,	2.048,	1.832],
[   48.159,	42.047,	36.165,	34.586,	31.3,	27.551,	22.713,	18.966,	15.001,	15.497,	12.871,	9.947,	8.369,	7.91,	5.403,	5.585,	4.773,	4.45,	3.986,	3.835,	3.503,	3.206,	3.055,	2.577,	2.518,	2.412,	2.209,	2.07,	1.97,	2.017,	1.702,	1.6,	1.58,	1.435,	1.378,	1.201,	1.293,	1.156,	1.001,	0.996],
[   50.332,	46.338,	39.563,	30.833,	29.563,	24.928,	20.413,	17.228,	14.146,	12.453,	9.055,	8.591,	5.766,	5.493,	4.404,	3.969,	3.086,	2.6,	2.159,	2.143,	1.967,	1.8,	1.782,	1.41,	1.557,	1.265,	1.067,	1.158,	1.025,	1.109,	0.978,	1.045,	0.908,	0.841,	0.719,	0.683,	0.723,	0.818,	0.605,	0.633],
[   53.628,	44.301,	36.812,	34.247,	29.407,	25.737,	22.233,	15.917,	14.698,	11.369,	9.046,	7.636,	6.76,	4.956,	3.958,	3.159,	2.171,	1.409,	1.243,	1.459,	1.392,	0.922,	0.668,	0.764,	0.816,	0.703,	0.685,	0.581,	0.657,	0.637,	0.56,	0.463,	0.578,	0.435,	0.484,	0.434,	0.421,	0.432,	0.439,	0.355]])

bar = np.array([
[   0.494,	0.567,	0.499,	0.526,	0.573,	0.6,	0.565,	0.567,	0.59,	0.571,	0.682,	0.7,	0.668,	0.608,	0.684,	0.681,	0.652,	0.663,	0.727,	0.631,	0.699,	0.73,	0.732,	0.731,	0.731,	0.703,	0.718,	0.776,	0.797,	0.724,	0.754,	0.721,	0.786,	0.775,	0.848,	0.814,	0.803,	0.858,	0.819,	0.876],
[   1.525,	1.56,	1.538,	1.697,	1.673,	1.63,	1.62,	1.724,	1.705,	1.751,	1.85,	1.828,	1.82,	1.902,	1.816,	1.841,	1.877,	2.018,	1.956,	2.037,	2.018,	2.112,	2.048,	2.133,	2.097,	2.117,	2.296,	2.26,	2.234,	2.218,	2.264,	2.194,	2.316,	2.381,	2.483,	2.407,	2.383,	2.461,	2.448,	2.525],
[   2.889,	3.083,	3.024,	3.101,	3.136,	3.238,	3.29,	3.215,	3.438,	3.369,	3.505,	3.404,	3.51,	3.551,	3.665,	3.674,	3.754,	3.856,	3.748,	3.937,	4.106,	3.932,	4.031,	4.19,	4.272,	4.284,	4.328,	4.298,	4.557,	4.32,	4.59,	4.695,	4.592,	4.786,	4.826,	4.642,	4.765,	4.891,	4.882,	4.839],
[   4.838,	5.058,	5.075,	5.166,	5.211,	5.351,	5.558,	5.349,	5.576,	5.409,	5.662,	5.635,	5.708,	6.075,	6.068,	6.175,	6.282,	6.156,	6.195,	6.473,	6.444,	6.494,	6.584,	6.753,	7.033,	7.023,	6.989,	7.084,	7.022,	7.155,	7.247,	7.455,	7.372,	7.619,	7.574,	7.823,	7.854,	7.742,	8.009,	8.015],
[   7.257,	7.345,	7.362,	7.442,	7.657,	7.605,	8.02,	7.994,	8.334,	8.361,	8.35,	8.305,	8.649,	8.643,	8.873,	8.951,	8.869,	9.066,	9.367,	9.401,	9.413,	9.588,	9.838,	9.788,	10.056,	10.279,	10.321,	10.393,	10.53,	10.708,	10.632,	10.982,	11.289,	11.072,	11.286,	11.3,	11.761,	11.705,	11.792,	12.021],
[   9.834,	10.039,	10.128,	10.164,	10.322,	10.542,	10.921,	11.065,	11.023,	11.329,	11.787,	11.558,	11.717,	11.998,	12.295,	12.537,	12.267,	12.503,	12.765,	12.818,	13.184,	13.194,	13.481,	13.769,	13.949,	13.89,	14.265,	14.226,	14.446,	14.661,	14.748,	15.059,	15.389,	15.302,	15.102,	15.694,	15.936,	16.154,	16.559,	16.246],
[   12.825,	12.942,	13.053,	13.551,	13.903,	13.856,	14.334,	14.469,	14.683,	15.004,	15.146,	15.002,	15.662,	15.403,	15.831,	16.241,	16.297,	16.668,	16.675,	16.851,	17.438,	17.506,	17.597,	17.613,	18.221,	18.4,	18.621,	18.987,	19.202,	19.522,	19.451,	19.753,	20.075,	20.303,	20.987,	20.522,	21.36,	20.899,	21.412,	21.532],
[   15.89,	16.514,	16.512,	17.256,	17.477,	17.79,	18.035,	18.293,	18.501,	18.812,	19.239,	19.415,	19.57,	20.37,	20.318,	20.412,	20.869,	21.001,	21.561,	21.746,	21.812,	22.548,	22.361,	22.812,	23.227,	23.558,	23.498,	24.293,	24.332,	24.625,	25.24,	25.696,	25.515,	25.997,	25.9,	26.384,	26.466,	26.791,	27.621,	27.749],
[   19.895,	20.147,	20.745,	21.135,	21.501,	21.852,	21.688,	22.537,	22.687,	22.92,	23.617,	23.988,	24.498,	24.686,	24.588,	25.943,	25.712,	26.582,	26.934,	26.719,	26.831,	27.448,	28.38,	28.446,	28.542,	29.611,	29.729,	30.502,	30.339,	30.623,	31.528,	31.787,	31.452,	32.059,	32.838,	33.33,	33.911,	33.87,	34.87,	34.995],
[   24.069,	24.476,	24.792,	25.237,	25.755,	26.387,	27.21,	27.53,	27.77,	27.864,	28.521,	28.852,	29.386,	29.884,	30.799,	31.46,	31.506,	32.281,	32.151,	32.813,	33.293,	33.739,	34.435,	34.63,	35.269,	35.523,	36.429,	37.367,	37.439,	38.293,	38.814,	38.999,	39.479,	40.908,	40.826,	41.367,	41.702,	42.244,	42.339,	43.107],
[   28.029,	28.686,	29.153,	30.402,	30.618,	31.505,	31.805,	32.287,	33.302,	33.03,	34.1,	35.261,	35.94,	36.423,	37.117,	37.836,	38.225,	38.174,	39.658,	40.003,	41.227,	41.236,	42.153,	43.126,	43.333,	44.435,	45.163,	45.642,	46.508,	46.855,	47.213,	48.444,	49.037,	49.963,	50.336,	51.804,	51.724,	52.37,	53.306,	55.039],
[   33.107,	33.588,	34.441,	35.754,	36.645,	37.111,	37.777,	38.668,	39.969,	40.943,	41.603,	41.74,	42.652,	43.861,	44.473,	46.312,	46.735,	46.953,	48.611,	49.508,	50.057,	50.93,	52.052,	52.568,	53.678,	54.743,	55.32,	57.029,	57.954,	57.991,	58.949,	60.164,	61.537,	61.851,	63.414,	64.058,	64.732,	65.584,	66.494,	66.865],
[   37.953,	39.185,	40.084,	41.597,	43.833,	44.645,	46.232,	48.268,	48.285,	49.787,	52.139,	52.193,	53.236,	54.878,	56.971,	56.624,	58.603,	60.379,	60.534,	62.659,	64.164,	64.574,	64.935,	65.971,	67.09,	67.624,	70.356,	71.373,	71.722,	71.984,	73.59,	74.799,	75.498,	76.002,	76.621,	77.147,	78.899,	79.865,	80.472,	81.559],
[   43.916,	46.003,	49.301,	52.169,	54.035,	55.868,	57.311,	60.87,	62.879,	63.368,	64.974,	67.95,	70.158,	70.001,	73.481,	73.207,	75.324,	74.793,	76.509,	78.052,	78.08,	79.616,	80.88,	80.49,	82.271,	83.127,	83.753,	84.312,	85.692,	86.046,	86.043,	86.646,	87.372,	88.579,	88.447,	88.495,	89.866,	90.105,	90.364,	91.207],
[   46.931,	50.046,	56.842,	58.45,	61.973,	64.817,	69.645,	71.766,	73.493,	77.36,	78.19,	80.595,	81.9,	83.468,	85.018,	85.993,	86.885,	88.364,	87.887,	89.023,	89.455,	90.216,	90.511,	91.455,	91.801,	91.857,	91.838,	92.339,	92.941,	92.884,	93.933,	93.988,	94.225,	94.24,	94.232,	95.078,	95.297,	95.725,	95.266,	95.596],
[   49.517,	55.555,	61.44,	63.211,	66.427,	70.18,	74.947,	78.809,	82.652,	82.257,	85.036,	87.885,	89.57,	90.001,	92.673,	92.444,	93.271,	93.701,	94.076,	94.228,	94.668,	94.893,	95.307,	95.661,	95.901,	96.01,	96.256,	96.395,	96.511,	96.464,	96.944,	96.934,	97.0,	97.182,	97.207,	97.53,	97.332,	97.614,	97.787,	97.832],
[   48.54,	52.589,	59.466,	68.044,	69.414,	74.064,	78.537,	81.811,	84.855,	86.606,	89.92,	90.469,	93.313,	93.57,	94.709,	95.113,	96.08,	96.593,	97.058,	97.052,	97.215,	97.411,	97.461,	97.757,	97.718,	98.008,	98.188,	98.123,	98.296,	98.233,	98.335,	98.228,	98.438,	98.519,	98.621,	98.669,	98.682,	98.565,	98.85,	98.77],
[   45.96,	55.266,	62.754,	65.316,	70.142,	73.75,	77.349,	83.653,	84.865,	88.175,	90.604,	91.996,	92.865,	94.645,	95.633,	96.49,	97.438,	98.292,	98.434,	98.207,	98.264,	98.778,	99.028,	98.892,	98.898,	98.995,	99.015,	99.148,	99.027,	99.034,	99.155,	99.233,	99.168,	99.281,	99.232,	99.274,	99.329,	99.302,	99.29,	99.39]])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(range(40), range(5, 95, 5))

ax.plot_surface(X, Y, bar, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')

plt.show()
