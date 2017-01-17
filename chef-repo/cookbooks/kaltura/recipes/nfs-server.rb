# Recipe contributed by Dudy Kohen <admin@panda-os.com>
# Creates needed users [borhan and apache] on the NFS server.
#
group "borhan" do
  gid 7373
end

user "borhan" do
  uid 7373
  home "#{node[:borhan][:BASE_DIR]}"
  supports :manage_home => false
  shell "/bin/bash"
  gid "borhan"
  comment "Borhan Server"
end

group "apache" do
  gid 48
  members "borhan"
end

user "apache" do
  uid 48
  shell "/sbin/nologin"
  home "/var/www"
  system true
  gid "apache"
  supports :manage_home => false
  comment "Apache"
end

directory "#{node[:borhan][:BASE_DIR]}" do
  owner "borhan"
  group "apache"
  mode 0775
  action :create
end

directory "#{node[:borhan][:BASE_DIR]}/web" do
  owner "borhan"
  group "apache"
  mode 0775
  action :create
end

nfs_export "#{node[:borhan][:BASE_DIR]}/web" do
  network '*'
  writeable true 
  sync true
  options ['no_root_squash']
end
