class linear_model():
    def __init__(self):
        self.a=np.array(50,3,1)
        self.b=np.array(50,50,1)

    def predict(self,x):
        return self.tranform(np.mult(self.a,x)+self.b)

    def transform(self, x):
        ret=np.array(50,50)
        for i in range(0,50):
            for j in range(0,50):
                ret[i][j]=x[i][j][1]
        return ret
    