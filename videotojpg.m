video_file = 'D:\code\pycode\infohide\video\hidevideo.avi';
video = VideoReader(video_file);% ��ȡ��Ƶ
frame_number = video.NumberOfFrames % �õ�֡��
for i=1:frame_number
   image_name = strcat('D:\code\pycode\infohide\framehide\frame', num2str(i-1));
   img_name = strcat(image_name,'.jpg');
   i
   I = read(video, i);% ����ͼƬ
   if i~=1
       imwrite(I, img_name, 'jpg');%дͼƬ������
   end
   imwrite(I, img_name, 'jpg');%дͼƬ������
   I = [];

end