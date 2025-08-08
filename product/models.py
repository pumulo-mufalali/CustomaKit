target = 7

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i = 0
for item in nums:
    for second_item in nums:
        i += 1
        if nums.count() < i:
            second_item = nums[i]
            if item + second_item == 7:
                print(f'{item}, {second_item}')
