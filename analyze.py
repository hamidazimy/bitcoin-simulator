import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import scipy
import scipy.interpolate

from scanf import scanf

"""
def nonuniform_imshow(x, y, z, aspect=1, cmap=plt.cm.rainbow):
  # Create regular grid
  xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
  xi, yi = np.meshgrid(xi, yi)

  # Interpolate missing data
  rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
  zi = rbf(xi, yi)

  _, ax = plt.subplots(figsize=(6, 6))

  hm = ax.imshow(zi, interpolation='nearest', cmap=cmap,
                 extent=[x.min(), x.max(), y.max(), y.min()])
  ax.scatter(x, y)
  ax.set_aspect(aspect)
  return hm


x = np.zeros(300)
y = np.zeros(300)
z = np.zeros(300)

results = np.zeros((300, 21, 50, 3))
spec_i = {}

with open("3miner with delay.txt") as F:
  for i in range(300):
    spec = scanf("%s ", F.readline())
    spec_i[spec[0]] = i

    for d in range(21):
      exps = np.array([[float(j) for j in i.split(',')] for i in F.readline().split(';')[:-1]])
      results[i, d, :, :] = exps
      # print(np.shape(results[i, d, :, :]))
      # print(np.shape(exps))
    F.readline()

    # break
print(results)
print(spec_i)
"""
#
#
#     means = np.mean(exps, axis=0)
#     print(means)
#
#     x[i] = 2 * spec[0]
#     y[i] = spec[1] - spec[2]
#     z[i] = means[0] / (spec[0])
#     print(z[i])
#
#
#
# heatmap = nonuniform_imshow(x, y, z)
# plt.colorbar(heatmap)
# plt.show()

# exit(0)
#
# data = np.zeros((31, 21, 30))
#
# with open("honest with delay.csv") as F:
#     for p in range(31):
#         for d in range(21):
#             vals = [float(x) for x in F.readline().strip()[:-1].split(',')]
#             data[p, d, :] = vals
#         #     print(vals)
#         # print('-' * 80)
#         F.readline()
#
# # print(data)
#
# means = np.mean(data, 2)
# vars = np.var(data, 2)
#
# for p in range(31):
#     print(','.join(["{:5.2f}".format(x) for x in means[p, :]]))
#
#
# fig = plt.figure()
# ax = fig.add_subplot(122, projection='3d')
# ax2 = fig.add_subplot(121, projection='3d')
#
#
# X = np.arange(0, 21, 1)
# Y = np.arange(50, 81, 1)
# X, Y = np.meshgrid(X, Y)
#
# ax.plot_surface(X, Y, means / np.arange(50, 81, 1)[:, None], rstride=1, cstride=1, cmap='plasma', edgecolor='none')
# ax2.plot_surface(X, Y, means, rstride=1, cstride=1, cmap='plasma', edgecolor='none')
#
# # ax.plot_surface(X, Y, (s / 100 - s_base) * 100, rstride=1, cstride=1, cmap='plasma', edgecolor='none')
#
# # ax.plot_wireframe(X, Y, np.array([[0] * 40] * 18), cmap='summer')
#
# # Z1 = (s / 100 - s_base) * 100
# # Z2 = np.array([[0] * 40] * 18)
# # #
# # ax.plot_surface(X,Y,np.where(Z1<Z2,Z1,np.nan), cmap="Pastel1")
# # # ax.plot_surface(X,Y,Z2)
# # ax.plot_surface(X,Y,np.where(Z1>=Z2,Z1,np.nan), cmap="Pastel2")
# #
# # plt.xlabel(r'$\delta$')
# # plt.ylabel(r'$\beta_t$')
#
# plt.show()