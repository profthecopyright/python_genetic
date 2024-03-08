% reference: https://www.mathworks.com/help/matlab/matlab_external/call-user-defined-custom-module.html
% A Demo Workflow

% add current path
if count(py.sys.path,pwd) == 0
    insert(py.sys.path,int32(0),pwd);
end

osdm = py.importlib.import_module('osd_matlab_interface');    % load package osd (optimal stimulus design)
py.importlib.reload(osdm);
c = jsondecode(fileread('gasg_config.json'));   % load config file. python json module does not work well

% it has to be like this
config = osdm.GAStimulusGeneratorConfig(...
    c.min_freq, c.max_freq, c.min_level, c.max_level, int32(c.component_num),...
    int32(c.population_size), int32(c.elite_num), int32(c.max_iter), c.frequency_sigma,...
    c.level_sigma, c.mutation_rate, c.cross_top...
);

stim_gen = osdm.GAStimulusGenerator(config);

total_batches = 20;
channel_num = 385;
disp('Experiment Started.')

test_unit = osdm.OShapedUnit();

for k = 1:total_batches
    stimuli = stim_gen.generate_stimuli();
    disp(['Batch ' num2str(k) ' of ' num2str(total_batches) ' Generated. Please present the stimuli and update the results.'])

    % ======== Convert parameters to waveforms ====================
    
    % To access the parameters of each stimulus, use e.g.
    f = double(stimuli{1}.frequencies);
    A = double(stimuli{1}.levels);
    p = double(stimuli{1}.phases);

    % ========= Deliver stimulus and do experiment =================
    
    % Change this section into real results.
    % It can be an array of size N, or a N-by-M matrix. N = population size
    % M can be 1 or actual number of channels, etc
    
    results = ones(c.population_size, channel_num);

    for s = 1:c.population_size
        results(s, :) = test_unit.rate(stimuli{s});
    end

    % all entries of valid results MUST BE POSITIVE
   
    % ===========================================================

    stim_gen.update_results(py.numpy.array(results));
    disp(['Batch ' num2str(k) ' of ' num2str(total_batches) ' Finished.'])
    disp(['Max Readout = ' num2str(max(mean(results, 2)))])
    disp('----------------------------------------------------------')
end

disp('Experiment Finished.')

% check stim_gen.all_records for the entire experiment history
