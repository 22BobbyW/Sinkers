# # import pandas as pd
# # import numpy as np
# # imu_data = pd.read_csv('clean_data.csv')
# # G = 9.80665 #m/s^2 --> gravitational acceleration

# # # np.linalg.norm(df[['X','Y','Z']].values,axis=1)

# # #Avg vertical acceleration
# # vert_accel = imu_data["Accel-Z"]
# # print(vert_accel.mean())
# # print(vert_accel.median())

# # mean_x = imu_data["Accel-X"].mean()
# # mean_y = imu_data["Accel-Y"].mean()
# # mean_z = imu_data["Accel-Z"].mean()

# # print(mean_x)
# # print(mean_y)
# # print(mean_z)

# # print("Accel Mean", np.sqrt(np.square(mean_x) + np.square(mean_y) + np.square(mean_z)))
# # print(np.linalg.norm(imu_data[["Accel-X", "Accel-Y", "Accel-Z"]].mean()))


# # #find angles between 2 vectors

# # mean = imu_data[["Accel-X", "Accel-Y", "Accel-Z"]].mean()
# # median = imu_data[["Accel-X", "Accel-Y", "Accel-Z"]].median()
# # gravity = [0,0,-1]

# # mean_tilt = 180 - np.degrees( np.arccos(
# #     (np.dot(gravity, mean) /
# #     np.linalg.norm(mean))
# # ))
# # print(mean_tilt)

# # median_tilt = 180 - np.degrees( np.arccos(
# #     (np.dot(gravity, median) /
# #     np.linalg.norm(median))
# # ))

# # # print(median_tilt)
# # import numpy as np
# # q1 = -2.6*10**(-6)
# # q2 = -7.5*10**(-6)
# # q3 = 3.1*10**(-6)
# # r = 0.02 #meters
# # K = 8.988*10**9

# # def getFq(qA, qB, rad):
# #     print(f"(K*q1*q2)/(r**2) = {K}*{qA}*{qB}/{r}**2 = ")
# #     res = K*qA*qB/(rad**2)
# #     print(res, "N")
# #     return res

# # print(q1)

# # Fq1 = getFq(q1, q3, r)
# # Fq2 = getFq(q2, q3, r)

# # Fq1x = Fq1*np.sin(np.radians(15))
# # Fq1y = Fq1*np.cos(np.radians(15))

# # Fq2x = Fq2*np.sin(np.radians(15))
# # Fq2y = Fq2*np.cos(np.radians(15))
# # print("Force   Fqx    Fqy")
# # print("Fq1", Fq1x,"N", Fq1y, "N")
# # print("Fq2", Fq2x,"N", Fq2y, "N")
# # print("Net Force (Vectors)")
# # print((Fq2x-Fq1x, Fq2y-Fq1y))
# import numpy as np
# def sin(angle):
#     return(np.sin(np.radians(angle)))

# def cos(angle):
#     return(np.cos(np.radians(angle)))
# m = 5.0
# g = 9.8 
# Fn = Fg = m*g 
# print(Fn)
# # print(12.4/(12*cos(40)))
# # print(12*sin(40))

# # Vi = 12*sin(40)
# # t = 1.3489208656433547
# # g = -9.8
# # h = Vi*t + (0.5)*g*(t**2)
# # print(h)
 
