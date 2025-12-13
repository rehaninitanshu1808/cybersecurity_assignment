class Ciphertext
  attr_reader :hexadecimal, :binary

  def initialize(hexadecimal)
    @hexadecimal = hexadecimal
    @binary = [hexadecimal].pack('H*')
  end

  def length
    hexadecimal.length
  end

  def self.to_binaries(hexadecimals)
    hexadecimals.map { Ciphertext.new(it).binary }
  end
end
