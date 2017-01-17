log "Installing Borhan MySQL DB"
if platform?("redhat", "centos", "fedora")
	bash "setup Borhan's repo" do
	     user "root"
	     code <<-EOH
		if ! rpm -q borhan-release;then
			rpm -ihv "#{node[:borhan][:BORHAN_RELEASE_RPM]}"
		else
			# if the package is already installed, maybe there's a new verison available.
			# in RPM, it try to update to the same version you have now - it stupidly returns RC 1 and hence the || true.
			rpm -Uhv "#{node[:borhan][:BORHAN_RELEASE_RPM]}" || true
		fi
		yum clean all
	     EOH
	end
end
package "borhan-db" do
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

bash "setup operational DB " do
     user "root"
     code <<-EOH
	#{node[:borhan][:BASE_DIR]}/bin/borhan-base-config.sh /root/borhan.ans
	#{node[:borhan][:BASE_DIR]}/bin/borhan-db-config.sh #{node[:borhan][:DB1_HOST]} #{node[:borhan][:SUPER_USER]} #{node[:borhan][:SUPER_USER_PASSWD]}  #{node[:borhan][:DB1_PORT]}
     EOH
end
