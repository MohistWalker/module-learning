##### 1.函数中的全局变量与局部变量 （local关键字）
##### 2.函数参数处理

    参数处理	说明
    $#	传递到脚本的参数个数
    $*	以一个单字符串显示所有向脚本传递的参数
    $$	脚本运行的当前进程ID号
    $!	后台运行的最后一个进程的ID号
    $@	与$*相同，但是使用时加引号，并在引号中返回每个参数。
    $-	显示Shell使用的当前选项，与set命令功能相同。
    $?	显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。
##### 3.使用命令行传递参数
    #!/bin/bash
    # using a global variable to pass a value
    function db1 {
            # $1和$2 不能从命令行中传递，只能调用函数时，手动传递
            echo $[ $1 * $2 ]
    }

    if [ $# -eq 2 ]
    then
            value=`db1 $1 $2`
            echo "The result is $value"
    else
            echo "Usage: badtest1 a b"
    fi
##### 4.函数中的数组
##### 5.函数的递归
    #!/bin/bash

    function factorial {
    	if [ $1 -eq 1 ]
    	then
    		echo 1
    	else
    		local temp=$[ $1 -1 ]
    		local result=`factorial $temp`
    		echo $[ $result * $1 ]
    	fi
    }

    read -p "Please input a value: " value
    result=`factorial $value`
    echo "The factorial of $value is: $result"