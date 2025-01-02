


% Path to the OBJ file
directory = '/Users/Wei Jie/Desktop/VM490 2024Jul Particiapant foot scan/aya/'; %change the address to the file directory
leftinputFileName1 = 'L1obj';
leftinputFileName2 = 'L2obj';
leftinputFileName3 = 'L3obj';
inputFilePath = fullfile(directory, inputFileName);

% Read the vertex data from the OBJ file
vertices = filereader(inputFilePath);

% Analyze the insole arches height
plot_insole_3d(vertices);

%analyze_insole_arches(vertices);


function [vertice] = filereader(file_path)
    % Open the file
    fileID = fopen(file_path, 'r');
    if fileID == -1
        error('Failed to open file: %s', file_path);
    end
    
    fprintf(file_path);

    vertice = [];
    
    % Read the file line by line
    while ~feof(fileID)
        line = fgetl(fileID);
        if startsWith(line, 'v ')
            % Split the line into components
            data = textscan(line, 'v %f %f %f');
            % Append the vertex to the vertices list
            vertice = [vertice; cell2mat(data)];
        end
    end
    
    % Close the file
    fclose(fileID);
end



function plot_insole_3d(vertices)
    % Extract x, y, z coordinates
    x = vertices(:, 1);
    y = vertices(:, 2);
    z = vertices(:, 3);

    z_min = min(z);
    z_max = max(z);
    y_min = min(y);
    y_max = max(y);
    insole_length = y_max - y_min;
    arch_height = z_max -(z_min);
    fprintf('The max y height of the insole is = %.2f , and the lowest y height of the insole is = %.2f units\n', z_max, z_min);
    fprintf('The total height of the insole is = %2f mm', arch_height);
    fprintf('insole length is = %f mm', insole_length);
    
    % Create a 3D scatter plot
    figure;
    scatter3(x, y, z, 1, z, 'filled'); % The last argument sets the color based on the z values
    title('3D Scatter Plot of Insole');
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    colorbar; % Adds a color bar to indicate the height
    grid on;
    axis equal;
    
    % Optionally, you can rotate the view to get a better perspective
    rotate3d on;
end

% function analyze_insole_arches(vertices)
%     % Extract x, y, z coordinates
%     x = vertices(:, 1);
%     y = vertices(:, 2);
%     z = vertices(:, 3);
%     
%     % Determine the range of y-values (width of the insole)
%     y_min = min(y);
%     y_max = max(y);
%     
%     % Number of bins to divide the width into (e.g., 100 bins)
%     num_bins = 100;
%     y_bins = linspace(y_min, y_max, num_bins);
%     
%     % Initialize array to store the maximum height in each bin
%     max_heights = zeros(num_bins, 1);
%     
%     % Find the maximum height (z-value) in each y-bin
%     for i = 1:num_bins
%         y_bin_min = y_bins(i);
%         if i == num_bins
%             y_bin_max = y_bins(i);
%         else
%             y_bin_max = y_bins(i+1);
%         end
%         bin_indices = find(y >= y_bin_min & y <= y_bin_max);
%         if ~isempty(bin_indices)
%             max_heights(i) = max(z(bin_indices));
%         else
%             max_heights(i) = NaN;
%         end
%     end
%     
%     % Plot the height profile across the width of the insole
%     figure;
%     plot(y_bins, max_heights, '-o');
%     title('Insole Arches Height Profile');
%     xlabel('Width of Insole (y)');
%     ylabel('Height (z)');
%     grid on;
%     
%     % Display the highest point as the arch height
%     [max_height, max_index] = max(max_heights);
%     arch_y_position = y_bins(max_index);
%     %fprintf('The maximum arch height is %.2f units at y = %.2f units\n', max_height, arch_y_position);
% end
