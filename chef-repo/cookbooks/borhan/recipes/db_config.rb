log "Configuring Borhan DB"
template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "borhan-base" do
  action :install
 end
package "borhan-postinst" do
  action :install
 end
#%w{ apr apr-util lynx }.each do |pkg|
#  package pkg do
#    action :install
#  end
#end

template "/root/borhan.ans" do
    source "borhan.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup Borhan DB" do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-base-config.sh /root/borhan.ans
	"#{node[:borhan][:BASE_DIR]}"/bin/borhan-db-config.sh #{node[:borhan][:DB1_HOST]} #{node[:borhan][:SUPER_USER]} #{node[:borhan][:SUPER_USER_PASSWD]} #{node[:borhan][:DB1_PORT]}
     EOH
end
