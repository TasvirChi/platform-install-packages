template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end

log "Installing Borhan front"
package "borhan-front" do
  action :install
  Chef::Config[:yum_timeout] = 3600
 end
%w{ borhan-front borhan-widgets borhan-html5lib borhan-html5-studio }.each do |pkg|
  package pkg do
    action :install
  end
end

template "/root/borhan.ans" do
    source "borhan.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup front node" do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-base-config.sh /root/borhan.ans
	"#{node[:borhan][:BASE_DIR]}"/bin/borhan-front-config.sh /root/borhan.ans
     EOH
end
