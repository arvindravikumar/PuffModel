def LeakPopulation(file_in=None, Leak_Col=None, file_out=None):
    import csv
    import pickle
    from inputclass import LeakInfo
    
    file = open(file_in)
    data = csv.reader(file, delimiter=',')
    
    rows = [x for x in data]
    leaktest = [x[Leak_Col] for x in rows]

    Leaks = [float(i) for i in leaktest]
             
    final = LeakInfo(Leaks)
    
    pickle.dump(final, open(file_out,'wb'))