log "Installing Borhan VOD Packager"
template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "borhan-nginx" do
  action :install
 end


template "/root/borhan.ans" do
    source "borhan.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup Nginx daemon" do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-nginx-config.sh /root/borhan.ans
     EOH
end
