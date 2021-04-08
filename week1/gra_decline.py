from sklearn import datasets
import numpy as np

from sklearn.linear_model import LinearRegression
lin = LinearRegression()


bosten = datasets.load_boston()
X = bosten.data
y = bosten.target
#X = x[y < 50.0]
#y = y[y < 50.0]

from sklearn.model_selection import train_test_split
X_train,X_text,y_train ,y_text = train_test_split(X , y , random_state= 888)


from sklearn.preprocessing import StandardScaler    #归一化处理
standardScaler = StandardScaler()
standardScaler.fit(X_train)
X_train_standard = standardScaler.transform(X_train)
X_text = standardScaler.transform(X_text)

X_standard = standardScaler.transform(X)


def F(th,X_b,y):
    try:
        fx = np.sum((y - X_b.dot(th))**2)/len(X_b)
        return fx
    except:
        return float('inf')

def dF(th , X_b ,y):
    a = np.empty(len(th))                  #用来装theta的
    a[0] = np.sum(X_b.dot(th) - y)
    for i in range(1,len(th)):
        a[i] = (X_b.dot(th) - y).dot(X_b[:,i])          #theta的计算
    return  a * 2 / len(X_b)

def gra_descent(X_b , y , init_th , eta , iters = 1e4 , ep = 1e-6):
    th = init_th
    i = 0
    while i < iters:
        td = dF(th ,X_b,y)
        last_th = th
        th = th - eta * td
        if(abs(F(th , X_b , y) - F(last_th , X_b , y)) < ep):
            break
        i += 1
    return th

def score_(X , y , intercept , coef):                    #计算R方
    y_ture = y
    y_pred = X.dot(coef) + intercept
    u = ((y_ture - y_pred ) ** 2).sum()
    v = ((y_ture - y_ture.mean()) ** 2).sum()
    RR = ( 1 - u / v)
    return RR

eta = 0.01                                         #"入"可决定下降步伐大小
X_b = np.hstack([np.ones((len(X_train_standard), 1)), X_train_standard])         #X矩阵加入X0，X0 = 1
inti_th = np.zeros(X_b.shape[1])                   #设置初始th值

th = gra_descent(X_b, y_train,inti_th ,eta)        #进行预测

intercept = th[0]
coef = th[1:]
lin.fit(X_train_standard,y_train)
print(f"用Linearegression预测bosten房价的函数\n参数为{lin.coef_}\n截距为({lin.intercept_})")
print(f"R方是{lin.score(X_text,y_text)})\n")
print(f"不用Linearegression预测bosten房价的函数\n参数为{coef}\n截距为({intercept})")
X_text_standard = standardScaler.transform(X_text)         #归一化
Rr = score_(X_text,y_text,intercept,coef)                  #计算R方
Mse = F(th,X_b,y_train)                                    #计算MSE
abe = abs(y - (X_standard.dot(coef) + intercept)).mean()   #绝对误差平均值为
print(f"R方为{Rr}\nMSE为{Mse}\n绝对误差平均值为{abe}\n")



