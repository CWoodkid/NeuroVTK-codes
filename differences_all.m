Differences = array2table(zeros([length(FileList)/2 9]), 'VariableNames', {'PrefI', 'Disttr', 'Speed', 'StandTime','MoveTime', 'StandPerDur','MovePerDur', 'StandPer', 'StandCount'});

Differences.PrefI = diff([[DATA.PrefI(1:2:73)],[DATA.PrefI(2:2:74)]],1,2)
Differences.Disttr = diff([[DATA.Disttr(1:2:73)],[DATA.Disttr(2:2:74)]],1,2)
Differences.Speed = diff([[DATA.Speed(1:2:73)],[DATA.Speed(2:2:74)]],1,2)
Differences.MoveTime = diff([[DATA.MoveTime(1:2:73)],[DATA.MoveTime(2:2:74)]],1,2)

%writetable(Differences,'Difference.csv')
writetable(DATA,'DATA.csv')

mdl = fitlm(Differences,'PrefI ~ Disttr');
plot(mdl)