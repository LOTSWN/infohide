video_file = 'D:\code\pycode\infohide\video\hidevideo.avi';
video = VideoReader(video_file);% 读取视频
frame_number = video.NumberOfFrames % 得到帧数
for i=1:frame_number
   image_name = strcat('D:\code\pycode\infohide\framehide\frame', num2str(i-1));
   img_name = strcat(image_name,'.jpg');
   i
   I = read(video, i);% 读出图片
   if i~=1
       imwrite(I, img_name, 'jpg');%写图片。保存
   end
   imwrite(I, img_name, 'jpg');%写图片。保存
   I = [];

end