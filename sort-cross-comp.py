#####################################################################################################
#
# Python script that implements selection sort, merge sort, and the merger function
# We also use this scipt to print figures out to compare runtimes
#
# python3
#####################################################################################################

######################## IMPORTS ########################
import matplotlib.pyplot as plt
import seaborn as sea
import numpy as np
import pandas as pd
import time

# selection sort implementation
def SelectionSort(nums):
    # start tracking time
    tic = time.perf_counter()

    # iterate through all list except the last element
    for low in range(len(nums)-1):
        mp = low
        # sort through current unsorted list
        for i in range(low+1, len(nums)):
            # compare and swap if smaller element is found
            if nums[i] < nums[mp]:
                mp = i
        # swap start of unsorted list element with the the min element found in the same portion
        (nums[low],nums[mp]) = (nums[mp],nums[low])

    # return time difference
    diff = time.perf_counter() - tic
    # check to see if sorted
    print('sorted:', all(nums[i] <= nums[i+1] for i in range(len(nums) - 1)))
    return diff

# buddy selection sort: split list -> selection sort on both -> merge sorted lists
def SelectionSplit(nums,size):

    # start time
    tic = time.perf_counter()
    # list when we merge two lists back together
    final = []
    # iterators for each list half
    start1,start2 = 0,0
    # split lists
    l1,l2 = nums[:size//2],nums[size//2:]

    # perform selection sort on first half
    for low in range(len(l1)-1):
        mp = low
        for i in range(low + 1, len(l1)):
            if l1[i] < l1[mp]:
                mp = i
        (l1[low],l1[mp]) = (l1[mp],l1[low])

    # perform selection sort on second half
    for low in range(len(l2)-1):
        mp = low
        for i in range(low + 1, len(l2)):
            if l2[i] < l2[mp]:
                mp = i
        (l2[low],l2[mp]) = (l2[mp],l2[low])

    # merge both sorted lists back together
    # while we have elements in either to merge
    while start1 < len(l1) and start2 < len(l2):
        # check if l1 is smaller
        if l1[start1] < l2[start2]:
            final.append(l1[start1])
            start1+= 1
        else:
            final.append(l2[start2])
            start2+= 1

    # add remaining elements from first half split
    while start1 < len(l1):
        final.append(l1[start1])
        start1+= 1

    # add remaining elements from second half split
    while start2 < len(l2):
        final.append(l2[start2])
        start2+= 1

    # record time difference
    diff = time.perf_counter() - tic
    # quick check to make sure actually sorted
    print('sorted:', all(final[i] <= final[i+1] for i in range(len(final) - 1)))

    return diff

# merge sort
def MergeSort(nums):
    # stoping case is when we have only 1 element
    if 1 == len(nums):
        return

    # recursive step if we have more than one element
    else:
        # split the lists
        a,b = nums[:len(nums)//2],nums[len(nums)//2:]
        # recursion
        MergeSort(a)
        MergeSort(b)
        # merge
        Merge(a,b,nums)

# merger
def Merge(l1,l2,l3):
    # starting positions
    start1,start2,start3 = 0,0,0

    # merge both sorted lists back together
    # while we have elements in either to merge
    while start1 < len(l1) and start2 < len(l2):
        # check if l1 is smaller
        if l1[start1] < l2[start2]:
            l3[start3] = l1[start1]
            start1+= 1
        else:
            l3[start3] = l2[start2]
            start2+= 1
        start3+= 1

    # add remaining elements from first half split
    while start1 < len(l1):
        l3[start3] = l1[start1]
        start1+= 1
        start3+= 1

    # add remaining elements from second half split
    while start2 < len(l2):
        l3[start3] = l2[start2]
        start2+= 1
        start3+= 1

def BigOrSmall(bos):
    # data that will depend on big or small run
    sizes = []
    file_name = ''
    # max random number possible
    upper = 1000000
    # number of replicates
    reps = 20

    # set seed so we can get consistent results
    # you can change this to get different random lists
    if bos: # big
        # random seed for reproducability
        np.random.seed(90)
        # different sizes we are assessing
        sizes = [100,200,400]
        # name of image we are saving
        file_name = 'big-sort-comp.png'
    else: # small
        # random seed for reproducability
        np.random.seed(94)
        # different sizes we are assessing
        sizes = [5,10,15,20]
        # name of image we are saving
        file_name = 'small-sort-comp.png'


    # data tracking
    times,N,sorter = [],[],[]
    # max random number possible
    upper = 1000000
    # number of replicates
    reps = 20

    # standard selection sort loop
    for i in range(len(sizes)):
        # what size are we on?
        size = sizes[i]
        print('size:',size)

        # get multiple data replicates
        for j in range(reps):
            print('rep:',j)

            # get random list of numbers of a designated size and range [0,upper]
            ran = np.random.randint(0,upper, size)
            # sort & time
            t = SelectionSort(ran)

            #record data for plots
            times.append(t)
            N.append(size)
            sorter.append('Selection Sort')
        print()

    # buddy selection sort loop
    for i in range(len(sizes)):
        # what size are we on?
        size = sizes[i]
        print('size:',size)

        # get multiple data replicates
        for j in range(reps):
            print('rep:',j)

            # get random list of numbers of a designated size and range [0,upper]
            nums = np.random.randint(0,upper, size)
            # sort & time
            t = SelectionSplit(nums,size)

            #record data for plots
            times.append(t)
            N.append(size)
            sorter.append('Buddy Selection Sort')

        print()

    # merge sort
    for i in range(len(sizes)):
        # what size are we on?
        size = sizes[i]
        print('size:',size)

        # get multiple data replicates
        for j in range(reps):
            print('rep:',j)

            # get random list of numbers
            nums = np.random.randint(0,upper, size)

            # sort & time
            tic = time.perf_counter()
            MergeSort(nums)
            toc = time.perf_counter()

            # make sure the list is sorted
            print('sorted:', all(nums[i] <= nums[i+1] for i in range(len(nums) - 1)))

            #record data
            times.append(toc - tic)
            N.append(size)
            sorter.append('Merge Sort')
        print()

    # create pandas data frame, as seaborn expects that
    df = pd.DataFrame({'List size': N, 'Seconds': times, 'Sort': sorter})
    # plot into a violin plot
    sea.violinplot(data=df, x='List size', y="Seconds", hue='Sort')
    plt.legend(loc='upper left')
    #save
    plt.savefig(file_name,dpi=1000,bbox_inches='tight')
    # plt.show() # uncomment if you want to see plot
    plt.clf()

def main():
    BigOrSmall(False)
    BigOrSmall(True)

if __name__ == "__main__":
    main()