from sklearn.metrics import precision_score, recall_score, f1_score

y_true = [1,0,1,1]
y_pred = [1,0,0,1]

print(precision_score(y_true, y_pred))
print(recall_score(y_true, y_pred))
print(f1_score(y_true, y_pred))