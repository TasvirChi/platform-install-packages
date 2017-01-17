#
# Cookbook Name:: borhan
# Recipe:: default
#
# Copyright 2014, Borhan, Ltd.
#
template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
log "Installing Borhan all in 1"
%w{ mysql-server borhan-server }.each do |pkg|
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

bash "setup All in 1" do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-mysql-settings.sh
	#{node[:borhan][:BASE_DIR]}/bin/borhan-config-all.sh /root/borhan.ans
     EOH
end
