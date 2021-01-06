% This code create ascii files containing the time in one column and the
% amplitude in the other columns. Resulting time will have the secuences alinging and
% clipped (Win)seconds.
%
% June 2019. Morelia ladomiguez@ucla.edu

clear all
close all
clc


addpath('~/CJA_Msac1.1/io/')
addpath('/mnt/data01/antonio/Dropbox/CRSMEX/matlab/')
addpath('/mnt/data01/antonio/Dropbox/lib/')

starting_directory = 466;

low      = 3; % See Snider Paper
high     = Inf;
Win      = 51.4;


fid      = fopen('directories.short', 'r');
stations = ['ARIG'; 'DAIG'; 'CAIG'; 'CRIG'; 'MEIG'; 'MMIG'; 'PNIG'; 'PLIG'; 'TLIG'; 'TXIG'; 'OXIG'; 'PEIG'; 'ZIIG'; 'YOIG'];
counter = 0;

while 1
    counter = counter +1;
    subdir  = fgetl(fid);
    if ~ischar(subdir)
        break
    end
    sequence_id = subdir(10:14);
    ids = load(fullfile(pwd,subdir,'unique_member_id.info'));
    if counter >= starting_directory
        for w = 1:size(stations,1)
            close all
            [files N] = ValidateComponent(stations(w,:),subdir);
            disp([subdir ' ' num2str(N) ' ' stations(w,:)])
            if N <= 1
                continue
            else
                disp(['N = ' num2str(N) ' files found.'])
            end
            
            a   = rsac(fullfile(pwd,subdir,files(1).name));
            a   = filter_sac(a,low,high,2);
            dta = a.dt;
            
            
            for k = 2:N
                b   = rsac(fullfile(pwd,subdir,files(k).name));
                b   = filter_sac(b,low,high,2);
                dtb = b.dt;
                
                [CorrelationCoefficient tshift S1 S2] = get_correlation_coefficient(a,b,Win,'combined',0);
                ta = 0:dta:(numel(S1) - 1)*dta;
                tb = 0:dtb:(numel(S2) - 1)*dtb;
                disp(['ts = ' num2str(tshift)])
                if k == 2
                    out_a          = [ta' S1]; 
                    id             = find(ids == str2num(a.kevnm));
                    if isempty(id)
                        error('No id found,check event ids.')
                    end
                    filename_out_a = strrep(a.filename, '.sac',['.' num2str(id,'%02d') '.table']);
                    save(filename_out_a, 'out_a', '-ascii'); 
                    disp(['Writting ... ' filename_out_a])
                end
            
                S2shift   = FourierShift(S2,tshift/dtb);
                out_b          = [tb' S2shift];

            	id             = find(ids == str2num(b.kevnm));
                if isempty(id)
                        error('No id found,check event ids.')
                end
                filename_out_b = strrep(b.filename, '.sac',['.' num2str(id,'%02d') '.table']);
                save(filename_out_b, 'out_b', '-ascii');
                disp(['Writting ... ' filename_out_b])
            end
            
            clear files a b
        end
    end
end
