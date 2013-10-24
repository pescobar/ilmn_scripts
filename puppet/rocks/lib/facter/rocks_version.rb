# rocks_version.rb

Facter.add("rocks_version") do
  setcode do
    Facter::Util::Resolution.exec('/opt/rocks/bin/rocks report version')
  end
end
