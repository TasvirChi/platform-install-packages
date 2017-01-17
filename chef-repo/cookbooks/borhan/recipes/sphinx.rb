template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
log "Installing Borhan Sphinx"
package "borhan-sphinx" do
  action :install
 end

template "/root/borhan.ans" do
    source "borhan.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup sphinx node" do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-mysql-settings.sh
        #{node[:borhan][:BASE_DIR]}/bin/borhan-base-config.sh /root/borhan.ans
        #{node[:borhan][:BASE_DIR]}/bin/borhan-sphinx-config.sh /root/borhan.ans
     EOH
end

