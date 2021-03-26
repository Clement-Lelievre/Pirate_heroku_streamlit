''' this script solves the pirates and the bullions puzzle (08/Jan/2020)'''
import time
import streamlit as st
import numpy as np
import pandas as pd
from time import sleep


# python functions to solve the puzzle

def nth_smallest(mylist,n,unique=False):
    '''this function returns the nth smallest value in the array, considering only unique values if unique=True'''
    return sorted(mylist)[n-1] if unique == False else sorted(list(set(mylist)))[n-1]


def index_nsmallest(mylist,n):
    ''' returns a list of indexes of the n smallest values (without removing duplicates) in mylist,regardless of the first element'''
    
    if n > len(mylist):
        return None
    l,mylist = [], mylist[1:]
    sorted_list = sorted(mylist)[:n]
    for item in mylist:
        if mylist.index(item) in l:
            continue
        elif item in sorted_list and sorted_list.count(item) == 1:
            l.append(mylist.index(item))
        elif item in sorted_list and sorted_list.count(item) > 1:
            for i in range(len(mylist)):
                if mylist[i] == item:
                    l.append(i)
    return l


def bribe_small(mylist,n):
    '''this function takes a list, identifies the n smallest values (without removing duplicates), increase their value by 1, 
    sets the rest at 0 except for the first element that is assigned n - whatever has been assigned. Ex : bribe_small([13,4,5,18,9,12],2,61) -> [50,5,6,0,0,0]'''
    ns, s = index_nsmallest(mylist,n) , sum(mylist)
    mylist=mylist[1:]
    for i in range(len(mylist)):
        mylist[i] = mylist[i] + 1 if i in ns else 0
    mylist = [s - sum(mylist)] + mylist
    return mylist


def solve_pirates(p,b,verbose=False): 
    '''this function solves the pirate puzzle, printing the steps if verbose=True'''
    if p > b:
        print('p must be <= b')
        return None
    starttime = time.time()
    split = [0] * (p-1) + [b]
    if verbose==True:
        print('Step 1 of',p,': current split is ',split,'\n')
        print('Step 2 of',p,': current split is ',split,'\n')
    
    
    for i in range(3,len(split)+1):
        split = [0] * (len(split) - i) + bribe_small(split[-i:],int(i/2))
        if verbose == True:
            print('Step',i,'of',p,': current split is ',split,'\n')
    
    endtime = time.time()
    exec_time = round(starttime - endtime,1)
    #print(f'First pirate will offer {split}.\nSolved in {exec_time} seconds.')
    return split

# p, b = None, None
# while type(p) != int or not p.isnumeric():
#     p = int(input('How many pirates are there?\n'))

# while type(b) != int or not b.isnumeric() or b<p:
#         b = int(input('And how many bullions to share (>= pirates)?\n'))

#solve_pirates(p,b,verbose=False)

# making the website

st.set_page_config(
            page_title="PIRATES PUZZLE", # => Quick reference - Streamlit
            page_icon=":parrot:",
            layout="centered", # wide
            initial_sidebar_state="auto") # c

st.title("The pirates enigma 🏴‍☠️")

st.markdown("""
    # ☠️☠️☠️☠️☠️☠️☠️
    # Pirates need to share their gold bullions.

    ## To do so, they proceed in the following way:

    ### Starting from the oldest pirate, each pirate offers a **split of the bullions**.
    ### Then, all pirates (still in the game) **vote either for or against this split**.
    ### If the split gets an *absolute* majority of votes, then the split is accepted, implemented and the game is over.
    ### Otherwise, the pirate whose split was just rejected is out of the game (he can no longer vote nor receive bullions), and it is the next pirate's (age-wise) turn to propose a split.
    ### 
""")

pirates = st.slider('Number of pirates', 1, 100)
bullions = st.slider('Number of bullions', pirates, 10*pirates, help = 'This should be more than the pirates count')

st.markdown("""
## How many bullions will the oldest pirate get?
""")
guess = st.number_input('Make your best guess',0,bullions,step=1)

while bullions<pirates:
    st.warning('There should be more bullions than pirates')

if st.button('Check answer'):
    with st.spinner('Calculating...') as s:
        split = solve_pirates(pirates, bullions)
    st.success('Calculation done! 👇') 
    st.bar_chart(pd.DataFrame(split))
    sleep(2)
    if guess == split[0]:
        st.balloons()
        st.success(f'You guessed it right! 😎 The oldest pirate will get {split[0]} bullions') 
    else:
        st.error('Incorrect guess 😯')


CSS = """
h1 {
    color: red;
}
body {
    background-image: url(https://www.keywestshipwreck.com/wp-content/uploads/2013/05/pirate_caribbean_johnny_depp_treasure_chest.jpg);
    background-size: cover;
}
"""

if st.checkbox('See Jack'):
    st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)