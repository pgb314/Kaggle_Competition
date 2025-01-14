def ml1():
    
    models = {'RFR':{'MODEL':RFR(),'PARAM':{'n_estimators': [10, 50, 100, 150, 200, 500],'max_depth':             [1,5,10,15,20],'min_weight_fraction_leaf':[0.0,0.1,0.2]}},
              'XGB':{'MODEL':XGBR(),'PARAM':{'n_estimators': [10, 50, 100, 150, 200, 500],'max_depth': [1, 5,6, 10, 15, 20],'learning_rate':[0.001,0.002,0.01,0.05] }},
              'SVR':{'MODEL':SVR(),'PARAM':{'kernel':['rbf','poly','linear']}},
              #'CTR':{'MODEL':CTR(),'PARAM:':{'depth' : [6,8,10],'learning_rate' : [0.01, 0.05, 0.1],'iterations': [30, 50, 100],'subsample' : [0.5, 0.7, 1.0]}},
              #'GaussianNB':{'MODEL':GaussianNB(),'PARAM':{'var_smoothing':[1e-09]}},
   
           'Lasso':{'MODEL':Lasso(),'PARAM':{'alpha':[0.3,0.5,0.7,0.9,1.0],'max_iter':[800,1000,1200]}},
              'LGBMR': {'MODEL':LGBMR(),'PARAM':{'boosting_type':['gbdt','dart'],'n_estimators':[10,50,100,150,200,500],}}}
    
            
            
                     
    rmse = []
    name = []
    #b = []
    score = []
    dfmodels = pd.DataFrame()
    for m in models:
        x = models[m]["MODEL"]
        p = models[m]["PARAM"]
        y_pred=grid(x,p).predict(X_test)
        #best= grid(x,p).best_params_   
        #sco = grid(x,p).best_score_
        MSE = mse(y_test, y_pred, squared=False)
        #score.append(sco)
        #b.append(best)
        rmse.append(MSE)
        name.append(m)
    dfmodels['Modelo'] = name
    dfmodels['RMSE'] = rmse
    #dfmodels['Best_Parametres'] = b
    #dfmodels['bestsco'] = score                        
    dfmodels.sort_values("RMSE",ascending=True,inplace=True,ignore_index=True)
    print(f'model {dfmodels.Modelo[0]} rmse {dfmodels.RMSE[0]} ')
    return dfmodels


def grid(modelo, param):
    
    g=GridSearchCV(modelo, # modelo de sklearn
                   param,  # dictio de parametros
                   cv=5,   # nº de cortes del cross-validation
                   return_train_score=True, # error en entrenamiento para checkear
                   n_jobs=-1  # usa todos los nucleos disponibles
                  )

    g.fit(X_train, y_train)
    print('Acierto test: {:.2f}'.format(g.score(X_test, y_test)))
    print('Acierto train: {:.2f}'.format(g.score(X_train, y_train)))
    print('Mejores parametros: {}'.format(g.best_params_))
    print('Modelo: {}'.format(modelo))
    print('Mejor acierto cv: {:.2f}'.format(g.best_score_))


   

    return g.best_estimator_.fit(X_train, y_train)


def label(df):    
    from sklearn.preprocessing import LabelEncoder

    for i in list(df.select_dtypes(exclude=["int64", 'float64']).columns):
        df[i] = LabelEncoder().fit_transform(df[i])common = pd.get_dummies(common, columns=common.select_dtypes(exclude=["int64", 'float64']).columns, drop_first = True)

    return df.head()
    
def scaler(df,num):    
    from sklearn.preprocessing import StandardScaler

    scaler=StandardScaler()

    df[num]=scaler.fit_transform(df[num])

    return df.head()

def dummies(df):
    df = pd.get_dummies(df,df.select_dtypes(exclude=["int64", 'float64']).columns, drop_first = True)
    return df


