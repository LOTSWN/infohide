temp1 = 'D:\code\pycode\infohide\frame\frame'; %ͼƬ·��
temp2 = '.jpg'; %ͼƬ��׺
WriterObj = VideoWriter('D:\code\pycode\infohide\video\hidevideo.avi');   %��ǰ�ļ�·���ϳ���Ƶ
WriterObj.FrameRate = 30;%�{�����ʣ��@�����Ը�׃�ϳ�ҕ�l���L��
n_frames = 267; % ͼ��֡������
open(WriterObj);
for i=0:n_frames-1 
   frame = imread(strcat(temp1, num2str(i), temp2)); % ��ȡͼƬ�����ڱ���frame��
   writeVideo(WriterObj, frame);% frame�ŵ�����WriteObj��
end
close(WriterObj);