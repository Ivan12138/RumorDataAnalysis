set src_file [lindex $argv 0]
set des_file [lindex $argv 1]

spawn scp qipeng@10.25.0.232:$src_file $des_file
expect "*assword:*"
send "senochow\r"
interact
expect eof