%% LocustBehaviourAnalysis

%Clear

clc; clear all; close all
%%

cd 'C:\Users\mcank\OneDrive\Masaüstü'\vtk\data_all\
FileList = dir('*.csv');
DATA=array2table(zeros([length(FileList) 10]), 'VariableNames', {'File','PrefI', 'Disttr', 'Speed', 'StandTime','MoveTime', 'StandPerDur','MovePerDur', 'StandPer', 'StandCount'});
DATA.File = {FileList.name}.';
%% 
notnumber=[];
for iFile= 1:length(DATA.File)    
    data=readtable(['C:\Users\mcank\OneDrive\Masaüstü\vtk\data_all\', DATA.File{iFile}]);
    
    Annotation=load(['C:\Users\mcank\OneDrive\Masaüstü\vtk\data_all\', strrep(DATA.File{iFile}, 'tracked.csv', 'annotation.mat')]);
    
    if ~isfloat(data.pos_x)
        notnumber=[notnumber iFile];
        continue
    end
    
    curr.posAnimal = [data.pos_x, data.pos_y];
    
    % smooth data
    curr.posAnimal(:,1) = movmedian(curr.posAnimal(:,1), 10);
    curr.posAnimal(:,2) = movmedian(curr.posAnimal(:,2), 10);
    
    %same length
    curr.posAnimal((length(curr.posAnimal)+1):18000,:)= nan;
    
    % Get location of shelters
    curr.posShelterGreg = Annotation.Annotation.Masks.Circular(1,1:2);
    curr.posShelterEmpty = Annotation.Annotation.Masks.Circular(2,1:2);
    
    % Normalize data
    curr.posAnimal = (curr.posAnimal-Annotation.Annotation.ROI.Par(1:2)) / Annotation.Annotation.ROI.Par(3);
    curr.posShelterGreg = (curr.posShelterGreg-Annotation.Annotation.ROI.Par(1:2)) / Annotation.Annotation.ROI.Par(3);
    curr.posShelterEmpty = (curr.posShelterEmpty-Annotation.Annotation.ROI.Par(1:2)) / Annotation.Annotation.ROI.Par(3);
    
    % Get distances to the two shelters 
    curr.dist2Greg = sqrt(sum((curr.posAnimal-curr.posShelterGreg)'.^2))';
    curr.dist2Empty = sqrt(sum((curr.posAnimal-curr.posShelterEmpty)'.^2))';
            
    %Präferenzindex
    curr.PrefI = (curr.dist2Empty-curr.dist2Greg)./(curr.dist2Greg + curr.dist2Empty);
    
    %Speed
    curr.speed = sqrt(sum(diff(curr.posAnimal)'.^2))'*450;
    
    %Stationary periods
    curr.stand = curr.speed<1;
    curr.move = curr.speed>=1;
    
    curr.standtime = regionprops(curr.stand);
    curr.movetime = regionprops(curr.move);
    
    DATA.PrefI(iFile)= mean(curr.PrefI, 'omitnan');
    DATA.Speed(iFile)= median(curr.speed(curr.stand==0), 'omitnan');                
    DATA.StandPer(iFile)= (sum(curr.stand)/(sum(curr.stand)+sum(curr.move)))*100;
    DATA.StandPerDur(iFile)=median([curr.standtime.Area], 'omitnan')/10;
    DATA.MovePerDur(iFile)=median([curr.movetime.Area], 'omitnan')/10;
    DATA.StandTime(iFile)= length(curr.speed(curr.stand==1))/10;
    DATA.MoveTime(iFile)=length(curr.speed(curr.stand==0))/10;
    DATA.StandCount(iFile)=length(curr.standtime);
    DATA.Disttr(iFile)=nansum(curr.speed);
end

%%
%PrefI
PrefIplot = figure();
boxplot([[DATA.PrefI(1:2:73)],[DATA.PrefI(2:2:74)]], ...
    'Labels',{'before Isolation ', 'after Isolation'})

ylabel('Preference Index')
exportgraphics(PrefIplot,'prefIplot_220107.jpg')
%ylim([1 60])

%Speed
Speedplot = figure();
boxplot([[DATA.Speed(1:2:73)],[DATA.Speed(2:2:74)]], ...
    'Labels',{'before Isolation ', 'after Isolation'})
ylabel(' Mean speed [cm/s]')
%ylim([1 60])
exportgraphics(Speedplot,'avgspeedplot_data1.jpg')

%% StatPerc
%StatPercplot = figure();
%boxplot([[DATA.StandPer(3:2:73)],[DATA.StandPer(4:2:74)]], ...
%    'Labels',{'before Isolation ', 'after Isolation'})
%ylabel('Percentage stationary')
%ylim([1 60])
%exportgraphics(StatPercplot,'statpercplot_data1.jpg')


%StandPerDur
%Standdurationplot = figure();
%boxplot([[DATA.StandPerDur(3:2:73)],[DATA.StandPerDur(4:2:74)]], ...
%    'Labels',{'before Isolation ', 'after Isolation'})
%ylabel('Average Duration of a stationary period [s]')
%%ylim([0 16])
%exportgraphics(Standdurationplot,'standdurplot_220107.jpg')

%MovePerDur
%Moverdurationplot = figure();
%boxplot([[DATA.MovePerDur(3:2:73)],[DATA.MovePerDur(4:2:74)]], ...
%    'Labels',{'before Isolation ', 'after Isolation'})
%ylabel('Average Duration of moving Period [s]')
%%ylim([0 16])
%exportgraphics(Moverdurationplot,'movedurplot_220107.jpg')



%Standtime
%Standtimeplot = figure();
%boxplot([[DATA.StandTime(1:2:73)],[DATA.StandTime(2:2:74)]], ...
%    'Labels',{'before Isolation ', 'after Isolation'})
%ylabel('Time spent standing [s]')
%%ylim([0 16])
%exportgraphics(Standtimeplot,'standtimeplot_220107.jpg')

%MoveTime
Movetimeplot = figure();
boxplot([[DATA.MoveTime(1:2:73)],[DATA.MoveTime(2:2:74)]], ...
    'Labels',{'before Isolation ', 'after Isolation'})
ylabel('Time spent moving [s]')
%ylim([1 80])
exportgraphics(Movetimeplot,'movetimeplot_220107.jpg')

%%StatCount
%StatCountplot = figure();
%boxplot([[DATA.StandCount(1:2:73)],[DATA.StandCount(2:2:74)]], ...
%    'Labels',{'before Isolation ', 'after Isolation'})
%ylabel('Number of stationary periods')
%%ylim([1 60])
%exportgraphics(StatCountplot,'statcountplot_220107.jpg')

Distplot = figure();
boxplot([[DATA.Disttr(1:2:73)],[DATA.Disttr(2:2:74)]], ...
    'Labels',{'before Isolation ', 'after Isolation'})
ylabel('Distance travelled')
exportgraphics(Distplot,'distplot_220107.jpg') 
