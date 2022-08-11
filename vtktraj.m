%% LocustBehaviourAnalysis

%Clear

clc; clear all; close all

%%
cd 'C:\Users\mcank\OneDrive\Masaüstü\vtk\set2\'
FileList = dir('*.csv');
DATA=array2table(zeros([length(FileList) 1]), 'VariableNames', {'File'});

DATA.File = {FileList.name}.';
DATA= [DATA(1,:); DATA(3,:);DATA(2,:);DATA(4,:); DATA(5,:); DATA(7,:); DATA(6,:); DATA(8,:)];


%% Analysis

figure1=figure();
fignum=1;
iplot=0;


for iFile = 1: height(DATA)
    iplot=iplot+1;
    
    if iplot>10
        iplot=1;
        fignum=fignum+1;
    end
    
    
          

        
    %Load data and Annotations
    data=readtable(['C:\Users\mcank\OneDrive\Masaüstü\vtk\set2\', DATA.File{iFile}]);
    
    Annotation=load(['C:\Users\mcank\OneDrive\Masaüstü\vtk\set2\', strrep(DATA.File{iFile}, 'tracked.csv', 'annotation.mat')]);
    
    % Get trajectory of the animal
    curr.posAnimal = [data.pos_x(:), data.pos_y(:)];
    
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
    
    %Rotate data (not necessary right now)
    % --- Get the current angle between the two shelters
    vec = curr.posShelterEmpty - curr.posShelterGreg;
    angle = atan2d(vec(2), vec(1));
    
    curr.posShelterGreg = rotation(angle, curr.posShelterGreg);
    curr.posShelterEmpty = rotation(angle, curr.posShelterEmpty);
    curr.posAnimal = rotation(angle, curr.posAnimal);
    
    % Check if gregarious shelter on right (rotated correctly)
    if curr.posShelterGreg(1) < curr.posShelterEmpty(1)
        angle = 180;
        
        curr.posShelterGreg = rotation(angle, curr.posShelterGreg);
        curr.posShelterEmpty = rotation(angle, curr.posShelterEmpty);
        curr.posAnimal = rotation(angle, curr.posAnimal);
    end% if 180 rotation is needed
        
        
        

   
    subplot(5,2, iplot);
    plot(curr.posAnimal(:,1)*-1, curr.posAnimal(:,2));
    %title();
    xlim([-1 1]);
    ylim([-1 1]);
   
end %File
        

set(gcf, 'position', [1,1,1000, 5000])

%%

%% Functions

% Function Rotation (using the angle and that needs to be rotated
function rot = rotation(angle, data)
    M = [ cosd(-angle) -sind(-angle);
        sind(-angle)  cosd(-angle) ]; 

    rot = (M*data(:,1:2)')';
    
end

