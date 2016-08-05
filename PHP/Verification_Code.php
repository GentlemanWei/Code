/**
 * @Author: LearnSlag
 * @Date:   2017-07-21 21:48:47
 * @Last Modified by:   LearnSlag
 * @Last Modified time: 2017-07-22 12:14:25
 */
<?php  
	# 创建一个随机码
	for ($i=0; $i < 4; $i++) { 
		# code...
		$_nmsg .= dechex(mt_rand(0,15));
	}
	# 将验证码保存到SESSION里
	$_SESSION['code'] = $_nmsg;
	# 设定验证码的图片的长度和高度
	$_width = 75;
	$_height = 25;
	# 创建图片
	$_img = imagecreatetruecolor($_width, $_height);
	# 创建一个白色
	$_white = imagecolorallocate($_img, 255, 255, 255);
	# 填充背景
	imagefill($_img,0,0,$_white);
	# 创建一个黑色边框
	$_black = imagecolorallocate($_img, 100, 100, 100);
	imagerectangle($_img, 0, 0, $_width-1, $_height-1, $_black);
	# 随机划线条
	for ($i=0; $i < 6; $i++) { 
		# code...
		$_md_color = imagecolorallocate($_img, mt_rand(0, 255), mt_rand(0, 255), mt_rand(0, 255));
		imageline($_img, mt_rand(0, 75), mt_rand(0, 75), mt_rand(0, 75), mt_rand(0, 75), $_md_color);
	}
	# 随机打雪花
	
	for ($i=0; $i < 100; $i++) { 
		# code...
		imagestring($_img, 1, mt_rand(1, $_width), mt_rand(1, $_height), "*" , 
			imagecolorallocate($_img, mt_rand(200, 255), mt_rand(200, 255), mt_rand(200, 255)));
	}
	# 输出验证码
	for ($i=0; $i < strlen($_SESSION['code']); $i++) {  
		# code...
		imagestring($_img, mt_rand(3, 5), $i * $_width / 4 + mt_rand(1, 10), mt_rand(1, $_height/2), $_SESSION['code'][$i],
			 imagecolorallocate($_img, mt_rand(0, 100), mt_rand(0, 150), mt_rand(0, 200)));
	}
	# 输出销毁	
	ob_clean();
	header("Content-Type:image/png");
	imagepng($_img);
	imagedestroy($_img);
?>