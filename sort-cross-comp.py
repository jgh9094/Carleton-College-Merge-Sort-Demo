#####################################################################################################
#
# Python script that implements selection sort, merge sort, and the merger function
# We also use this scipt to print figures out to compare runtimes
#
# python3
#####################################################################################################

######################## IMPORTS ########################
from re import A
import matplotlib.pyplot as plt
import seaborn as sea
import numpy as np
import pandas as pd
import time

# loop through differnt files that exist
def SelectionSort(nums):
    tic = time.perf_counter()
    for low in range(len(nums)-1):
        mp = low
        for i in range(low + 1, len(nums)):
            if nums[i] < nums[mp]:
                mp = i
            nums[low],nums[mp] = nums[mp],nums[low]

    # return time difference
    return time.perf_counter() - tic

# selection sort with one split
def SelectionSplit(l1, l2):

    # start time
    final = []
    start1,start2 = 0,0
    tic = time.perf_counter()

    for low in range(len(l1)-1):
        mp = low
        for i in range(low + 1, len(l1)):
            if l1[i] < l1[mp]:
                mp = i
        l1[low],l1[mp] = l1[mp],l1[low]

    for low in range(len(l2)-1):
        mp = low
        for i in range(low + 1, len(l2)):
            if l2[i] < l2[mp]:
                mp = i
        l2[low],l2[mp] = l2[mp],l2[low]

    while start1 != len(l1) and start2 != len(l2):
        # check if l1 is smaller
        if l1[start1] < l2[start2]:
            final.append(l1[start1])
            start1+= 1
        else:
            final.append(l2[start2])
            start2+= 1

    # get remaining vals in l1
    while start1 < len(l1):
        final.append(l1[start1])
        start1+= 1

    # get remaining vals in l2
    while start2 < len(l2):
        final.append(l2[start2])
        start2+= 1

    return time.perf_counter() - tic

# merge sort
def MergeSort(nums):
    # recursive step
    if 1 < len(nums):
        a,b = nums[:len(nums)//2],nums[len(nums)//2:]
        MergeSort(a)
        MergeSort(b)
        Merge(a,b,nums)

# merger
def Merge(l1,l2,l3):
    # starting positions
    start1,start2,start3 = 0,0,0

    while start1 != len(l1) and start2 != len(l2):
        # check if l1 is smaller
        if l1[start1] < l2[start2]:
            l3[start3] = l1[start1]
            start1+= 1
        else:
            l3[start3] = l2[start2]
            start2+= 1
        start3+= 1

    # get remaining vals in l1
    while start1 < len(l1):
        l3[start3] = l1[start1]
        start1+= 1
        start3+= 1

    # get remaining vals in l2
    while start2 < len(l2):
        l3[start3] = l2[start2]
        start2+= 1
        start3+= 1

def main():
    # set seed so we can get consistent results
    np.random.seed(94)
    # list of list sizes we care about
    # sizes = [5,10,15,20] # small
    sizes = [100,200,300,400] # big
    times,N,sorter = [],[],[]
    upper = 100000000
    reps = 10

    # standard selection sort reps
    for i in range(len(sizes)):
        size = sizes[i]
        print('size:',size)
        for j in range(reps):
            print('rep:',j)
            # get random list of numbers
            nums = np.random.randint(0,upper, size)

            # sort
            t = SelectionSort(nums)

            #record data
            times.append(t)
            N.append(size)
            sorter.append('Selection')
        print()

    # single split selection sort reps
    for i in range(len(sizes)):
        size = sizes[i]
        print(size)
        for j in range(reps):
            print('rep:',j)
            # get random list of numbers
            nums = np.random.randint(0,upper, size)
            l1,l2 = nums[:size//2],nums[size//2:]

            # sort
            t = SelectionSplit(l1,l2)

            #record data
            times.append(t)
            N.append(size)
            sorter.append('Half')
        print()

    # single split selection sort reps
    for i in range(len(sizes)):
        size = sizes[i]
        print(size)
        for j in range(reps):
            print('rep:',j)
            # get random list of numbers
            nums = np.random.randint(0,upper, size)

            # sort
            tic = time.perf_counter()
            MergeSort(nums)
            toc = time.perf_counter()

            #record data
            times.append(toc - tic)
            N.append(size)
            sorter.append('Merge')
        print()

    # plot data in a violin plot
    df = pd.DataFrame({'List size': N, 'Seconds': times, 'Sort': sorter})
    sea.lineplot(data=df, x='List size', y="Seconds", hue='Sort')
    plt.xticks(sizes)
    plt.legend(loc='upper left')
    
    # plt.savefig('small-sort-comp.png',dpi=500,bbox_inches='tight')
    plt.savefig('big-sort-comp.png',dpi=1000,bbox_inches='tight')
    # plt.show()

if __name__ == "__main__":
    main()