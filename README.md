# lucky_you

一个简单的点名/抽奖程序 based on wxpython

## Dependence

- wxpython (http://wxpython.org/)

## Usage

- 在pic文件夹下放置相应人员的照片，推荐使用jpg格式
- 在text文件夹下放置与相应人员照片文件名相同但后缀为txt的信息

## Example

- pic/1.jpg <--> text/1.txt
- pic/2.jpg <--> text/2.txt

## About exe for windows

- 用py2exe打包的exe版本，可以在无python和wxpython的环境中使用
- 下载地址：https://github.com/huxuan/luckyi\_you/downloads
- 文件名示例：lucky\_you\_[版本号].zip
- 运行可能导致杀毒软件报毒，请添加白名单放心使用
- 压缩包中包含的w9xpopen.exe和python27.dll均为依赖文件
- 将对应的图片和文本放到pic和text文件夹下后，双击运行lucky\_you.exe即可
- 可以解压后的文件夹放置在任意位置，把luck\_you.exe的快捷方式放到桌面上使用
  （无需移动pic和text文件夹）

## Known Issues

- py2exe后的exe版本图片未居中（应该是py2exe的问题，不影响使用）
- 还需要实现更多的自定义参数
- 实现快捷键开始和停止
