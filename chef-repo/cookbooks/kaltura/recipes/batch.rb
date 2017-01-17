log "Installing Borhan batch"
#if platform?("redhat", "centos", "fedora")
#	bash "setup Borhan's repo" do
#	     user "root"
#	     code <<-EOH
#	     echo Platform is #{node['platform']}
#		if ! rpm -q borhan-release;then
#			rpm -ihv "#{node[:borhan][:BORHAN_RELEASE_RPM]}"
#		else
#			# if the package is already installed, maybe there's a new verison available.
#			# in RPM, it try to update to the same version you have now - it stupidly returns RC 1 and hence the || true.
#			rpm -Uhv "#{node[:borhan][:BORHAN_RELEASE_RPM]}" || true
#		fi
#		yum clean all
#	     EOH
#	end
#end
template "/etc/yum.repos.d/borhan.repo" do
    source "borhan.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "borhan-batch" do
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

bash "setup batchMgr daemon" do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-base-config.sh /root/borhan.ans
	#{node[:borhan][:BASE_DIR]}/bin/borhan-batch-config.sh /root/borhan.ans
     EOH
end
