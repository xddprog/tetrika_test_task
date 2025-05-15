def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']
    
    def merge_intervals(intervals):
        if not intervals:
            return []
            
        pairs = [(intervals[i], intervals[i+1]) for i in range(0, len(intervals), 2)]
        pairs.sort()
        
        merged = [list(pairs[0])]
        for current in pairs[1:]:
            if current[0] <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], current[1])
            else:
                merged.append(list(current))
        return merged
    
    lesson_start, lesson_end = lesson
    pupil_intervals = merge_intervals(pupil)
    tutor_intervals = merge_intervals(tutor)
    
    pupil_intervals = [[max(p[0], lesson_start), min(p[1], lesson_end)] 
                      for p in pupil_intervals 
                      if p[0] <= lesson_end and p[1] >= lesson_start]
    
    tutor_intervals = [[max(t[0], lesson_start), min(t[1], lesson_end)] 
                      for t in tutor_intervals 
                      if t[0] <= lesson_end and t[1] >= lesson_start]
    
    total_time = 0
    i = j = 0
    
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        p_start, p_end = pupil_intervals[i]
        t_start, t_end = tutor_intervals[j]
        
        start = max(p_start, t_start)
        end = min(p_end, t_end)
        
        if start <= end:
            # Если точки совпадают, считаем за 1 секунду пересечения
            total_time += max(1, end - start) if start == end else end - start
            
        if p_end < t_end:
            i += 1
        else:
            j += 1
            
    return total_time

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [150, 170],
             'tutor': [150, 170]},
     'answer': 20
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [110, 120],
             'tutor': [130, 140]},
     'answer': 0
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [110, 120, 130, 140, 150, 160],
             'tutor': [115, 125, 135, 145, 155, 165]},
     'answer': 15
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [50, 150],
             'tutor': [150, 250]},
     'answer': 1
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [120, 160, 130, 140],
             'tutor': [110, 170]},
     'answer': 40
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [100, 200],
             'tutor': [100, 200]},
     'answer': 100
    },
    {'intervals': {'lesson': [100, 200],
             'pupil': [100, 101, 150, 151],
             'tutor': [100, 101, 150, 151]},
     'answer': 2
    }
]

if __name__ == '__main__':
    for i, test in enumerate(tests, 1):
        test_answer = appearance(test['intervals'])
        print(f'Test case {i}: {test_answer} {test["answer"]}')
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
