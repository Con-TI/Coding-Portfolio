import pandas as pd
import yfinance as yf
import numpy as np
import graphviz 
import pandas_ta as ta
import random

'''
Levels:
- {Very High, High, Medium, Low, Very Low}
Indicators:
- {RSI, STO, ATR}
'''

min_depth = 2
max_depth = 4
treeNum = 100
numGens = 2
swap_p = 0.5
mutate_p = 0.5
df = yf.download('^GSPC',start="2020-01-01").dropna()
test_df= yf.download('^GSPC',start="2000-01-01",end="2020-01-01").dropna()
rsi = ta.rsi(df['Close'],length=14)
sto = ta.stoch(df['High'],df['Low'],df['Close']).iloc[:,0]
atr = ta.atr(df['High'],df['Low'],df['Close'],length=14)
test_rsi = ta.rsi(test_df['Close'],length=14)
test_sto = ta.stoch(test_df['High'],test_df['Low'],test_df['Close']).iloc[:,0]
test_atr = ta.atr(test_df['High'],test_df['Low'],test_df['Close'],length=14)
# del rsi,sto,atr

def _indicator_level_func(indicator,n=14):
    # ["Very High", "High", "Medium", "Low", "Very Low"]
    zeros = np.zeros(indicator.shape)
    zeros[:] = np.nan
    leveldf = pd.DataFrame(zeros,indicator.index).astype(str)
    levels = ["VL","L","M","H,","VH"]
    rollingMax = indicator.rolling(n).max().shift(1)
    rollingMin = indicator.rolling(n).min().shift(1)
    normedIndicator = (indicator-rollingMin)/(rollingMax-rollingMin)
    leveldf[normedIndicator<=0.2] = "VL"
    leveldf[(normedIndicator<=0.4) & (normedIndicator>0.2)] = "L"
    leveldf[(normedIndicator<=0.6) & (normedIndicator>0.4)] = "M"
    leveldf[(normedIndicator<=0.8) & (normedIndicator>0.6)] = "H"
    leveldf[normedIndicator>0.8] = "VH"
    return leveldf

class TreeNode:
    def __init__(self,condition=None,left=None,right=None):
        # left is condition false, right is condition true
        self.condition = condition
        self.left = left
        self.right = right
        self.depth = None
    def predict(self,value):
        if value == self.condition[1]:
            return self.right
        else: 
            return self.left

def _forward_pass(tree,values):
    if tree.condition[0] == 'rsi':
        output = tree.predict(values[0])
    elif tree.condition[0] == 'sto':
        output = tree.predict(values[1])
    elif tree.condition[0] == 'atr':
        output = tree.predict(values[2])
    while (output!=0)&(output!=1):
        if output.condition[0] == 'rsi':
            output = output.predict(values[0])
        elif output.condition[0] == 'sto':
            output = output.predict(values[1])
        elif output.condition[0] == 'atr':
            output = output.predict(values[2])
    return output

def _build_tree(min_depth,max_depth):
    indicators = ['rsi','sto','atr']
    conditions = ["VL","L","M","H,","VH"]
    condition = (random.choice(indicators),random.choice(conditions))
    tree = TreeNode(condition=condition)
    if min_depth == max_depth:
        tree_depth = max_depth
    else:
        tree_depth = random.randint(min_depth,max_depth)
    curr_depth = 0
    prev_nodes = []
    while curr_depth < tree_depth-1:
        if curr_depth==0:
            condition = (random.choice(indicators),random.choice(conditions))
            setattr(tree,"left",TreeNode(condition=condition))
            condition = (random.choice(indicators),random.choice(conditions))
            setattr(tree,"right",TreeNode(condition=condition))
            prev_nodes.append(getattr(tree,"left"))
            prev_nodes.append(getattr(tree,"right"))
        else:
            for prev_node in prev_nodes:
                condition = (random.choice(indicators),random.choice(conditions))
                setattr(prev_node,"left",TreeNode(condition=condition))            
                condition = (random.choice(indicators),random.choice(conditions))
                setattr(prev_node,"right",TreeNode(condition=condition))
            store_list = []
            for prev_node in prev_nodes:
                store_list.append(getattr(tree,"left"))
                store_list.append(getattr(tree,"right"))
            prev_nodes = store_list
        curr_depth+=1
    for prev_node in prev_nodes:
        setattr(prev_node,"left",random.randint(0,1))
        setattr(prev_node,"right",random.randint(0,1))
    setattr(tree,"depth",tree_depth)
    return tree

def swap(tree1,tree2,min_depth):
    tree = tree1
    max_depth = min(tree1.depth,tree2.depth)
    depth_choice = random.randint(min_depth,max_depth)
    curr_depth = 0
    while curr_depth<depth_choice-2:
        direc = random.choice(['left','right'])
        nodeT1 = getattr(tree,direc)
        nodeT2 = getattr(tree2,direc) 
        curr_depth+=1
    if 0 == (depth_choice-2):
        setattr(tree,random.choice(['left','right']),getattr(tree2,random.choice(['left','right'])))
    else:
        setattr(nodeT1,random.choice(['left','right']),getattr(nodeT2,random.choice(['left','right'])))
    return tree

def mutate(tree):
    typeRef = type(TreeNode())
    indicators = ['rsi','sto','atr']
    conditions = ["VL","L","M","H,","VH"]
    curr_depth = 0
    stop = random.randint(1,tree.depth)
    while curr_depth<stop:
        direc = random.choice(['left','right'])
        node = getattr(tree,direc)
        curr_depth += 1 
    if type(node.left) == typeRef:
        condition = (random.choice(indicators),random.choice(conditions))
        setattr(node,"condition",condition)
    else:
        setattr(node,random.choice(['left','right']),random.randint(0,1))

def initialize_trees(treeNum = treeNum,max_depth=max_depth,min_depth=min_depth):
    trees = []
    for i in range(treeNum):
        trees.append(_build_tree(min_depth,max_depth))
    return trees

def backtest(df,signal):
    # market_ret = df.iloc[-1]/df.iloc[0]
    rets = df.pct_change().shift(-1).dropna()
    # return (rets*signal+1).cumprod().iloc[-1], market_ret
    return (rets*signal+1).cumprod().iloc[-1]


def forward_pass_trees(trees,indicatordf,close_data,to_concat):
    scores = []
    for tree in trees:
        signal_df = []
        for idx,row in indicatordf.iterrows():
            signal_df.append(_forward_pass(tree,list(row)))
        signal = pd.concat([to_concat,pd.Series(signal_df,index=indicatordf.index)],axis=0).iloc[:-1]
        scores.append(backtest(close_data,signal))
    return scores

def test_pass(tree,indicatordf,close,to_concat):
    signal_df = []
    for idx,row in indicatordf.iterrows():
        signal_df.append(_forward_pass(tree,list(row)))
    signal = pd.concat([to_concat,pd.Series(signal_df,index=indicatordf.index)],axis=0).iloc[:-1]
    return backtest(close,signal)

def next_gen(trees,scores):
    scores = np.exp(np.array(scores))**2
    if (scores.max()-scores.min())!=0:
        scores = list((scores - scores.min())/(scores.max()-scores.min()))
    new_trees = []
    for i in range(len(trees)):
        tree1 = random.choices(trees,weights=scores)[0]
        tree2 = random.choices(trees,weights=scores)[0]
        if np.random.uniform(0,1)>swap_p:
            childTree = random.choice([tree1,tree2])
        else:
            childTree = swap(tree1,tree2,min_depth)
        if np.random.uniform(0,1)>mutate_p:
            new_trees.append(childTree)
        else:
            mutate(childTree)
            new_trees.append(childTree)
    return new_trees

def main():
    global rsi, sto, atr, test_rsi, test_sto, test_atr, df, test_df, numGens
    close_data = df['Close']
    rsi=_indicator_level_func(rsi)
    sto=_indicator_level_func(sto)
    atr=_indicator_level_func(atr)
    
    indicatordf = pd.concat([rsi,sto,atr],axis=1)
    non_nan = ~((indicatordf == "nan").any(axis=1))
    to_concat = indicatordf[(indicatordf == "nan").any(axis=1)].iloc[:,0]
    to_concat[:] = 0
    indicatordf = indicatordf[non_nan]
    del non_nan, df

    trees = initialize_trees()
    best_tree = {'return':0}
    print(f'Train market return: {close_data.iloc[-1]/close_data.iloc[0]}')
    for i in range(numGens):
        scores = forward_pass_trees(trees,indicatordf,close_data,to_concat)
        print(f"Gen {i+1} done, best return: {max(scores)}")
        if max(scores)>best_tree['return']:
            best_tree["tree"] = trees[scores.index(max(scores))]
            best_tree["return"] = max(scores)
        if i != 9:
            trees = next_gen(trees,scores)
    print(best_tree)
    del rsi, sto, atr

    test_close = test_df['Close']
    test_rsi=_indicator_level_func(test_rsi)
    test_sto=_indicator_level_func(test_sto)
    test_atr=_indicator_level_func(test_atr)
    indicatordf = pd.concat([test_rsi,test_sto,test_atr],axis=1)
    non_nan =~((indicatordf == "nan").any(axis=1))
    to_concat = indicatordf[(indicatordf == "nan").any(axis=1)].iloc[:,0]
    to_concat[:] = 0
    indicatordf = indicatordf[non_nan]
    del non_nan, test_df

    test_score = test_pass(best_tree['tree'],indicatordf,test_close,to_concat)
    # test_scores = forward_pass_trees(trees,indicatordf,test_close,to_concat)
    # test_score = max(test_scores)
    print(f"Test Score: {test_score}, Market Return: {test_close.iloc[-1]/test_close.iloc[0]}")
    del test_rsi, test_sto, test_atr


if __name__=="__main__":
    main()