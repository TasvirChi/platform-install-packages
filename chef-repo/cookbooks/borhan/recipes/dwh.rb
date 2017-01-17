log "Installing Borhan DWH"
template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "borhan-dwh" do
  action :install
  Chef::Config[:yum_timeout] = 3600
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

bash "setup DWH " do
     user "root"
     code <<-EOH
	echo "NO" | #{node[:borhan][:BASE_DIR]}/bin/borhan-base-config.sh /root/borhan.ans
	#{node[:borhan][:BASE_DIR]}/bin/borhan-dwh-config.sh /root/borhan.ans
     EOH
end
