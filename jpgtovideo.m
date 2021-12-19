temp1 = 'D:\code\pycode\infohide\frame\frame'; %图片路径
temp2 = '.jpg'; %图片后缀
WriterObj = VideoWriter('D:\code\pycode\infohide\video\hidevideo.avi');   %当前文件路径合成视频
WriterObj.FrameRate = 30;%調整幀率，這個可以改變合成視頻的長短
n_frames = 267; % 图像帧的总数
open(WriterObj);
for i=0:n_frames-1 
   frame = imread(strcat(temp1, num2str(i), temp2)); % 读取图片，放在变量frame中
   writeVideo(WriterObj, frame);% frame放到变量WriteObj中
end
close(WriterObj);