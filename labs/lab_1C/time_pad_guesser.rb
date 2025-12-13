require_relative 'ciphertext'

class TimePadGuesser
  attr_reader :binaries, :decrypted_messages

  def initialize(hexadecimals)
    # Convert the hexadecimal ciphers to binaries.
    @binaries = Ciphertext.to_binaries(hexadecimals)

    # Prepare an array of empty mesages, one per cipher, still to decode.
    @decrypted_messages = binaries.map { Array.new(it.length) }
  end

  # The main interactive loop for the user.
  def run
    loop do
      display_decrypted_messages

      prompt_user_for_guesses
    rescue Interrupt
      puts "\nExiting."
      break
    end
  end

  private

  # Formats and prints all partially decrypted messages.
  def display_decrypted_messages
    display_divider

    decrypted_messages.each_with_index do |bytes, message_number|
      plain_text_guess = bytes.map { printable_character(it) }.join

      puts format('Msg %02d: %s', message_number, plain_text_guess)
    end

    display_divider
  end

  # Prompts the user for a new guess and updates the state accordingly.
  def prompt_user_for_guesses
    puts "Enter your next guess (or Ctrl+C to exit)."
    puts "Visual help: the first unknown position for each message is currently #{decrypted_messages.first.index(nil)}"

    display_divider

    print "Enter number of message to guess (0-#{decrypted_messages.size - 1}): "
    message_number = gets.to_i

    print "Enter starting position of your guess in the message: "
    position = gets.to_i

    print 'Enter the guessed text: '
    guessed_text = gets.chomp

    update_with_latest_guess(message_number, position, guessed_text)
  end

  # A simple visual divider for better readability.
  def display_divider
    offset = 8
    max_decoded_message_length = binaries.map(&:length).max

    puts ''
    puts '*' * (max_decoded_message_length + offset)
    puts ''
  end

  # Converts a byte to a printable character, using '.' for yet unknown bytes.
  def printable_character(byte)
    return '.' unless byte&.between?(32, 126)

    byte.chr
  end

  # Updates all decrypted_messages based on a new guess.
  def update_with_latest_guess(message_number, position, guessed_text)
    key_segment = recover_key_segment(message_number, position, guessed_text)

    update_all_decrypted_messages(position, key_segment)
  end

  # Recover the key segment by XORing the guessed plaintext against its ciphertext.
  def recover_key_segment(message_number, position, guessed_text)
    target_ciphertext = @binaries[message_number][position, guessed_text.length]

    xor_strings(target_ciphertext, guessed_text)
  end

  # Use the new key segment to update all decrypted_messages at that position.
  def update_all_decrypted_messages(position, key_segment)
    @binaries.each_with_index do |cipher, i|
      cipher_segment = cipher[position, key_segment.length]
      plain_segment = xor_strings(cipher_segment, key_segment)

      plain_segment.bytes.each_with_index do |byte, j|
        @decrypted_messages[i][position + j] = byte
      end
    end
  end

  # XORs two binary strings and returns the result.
  def xor_strings(s1, s2)
    # Convert strings to arrays of byte values, zip them, perform XOR,
    # and pack the result back into a binary string.
    s1.bytes.zip(s2.bytes).map { |b1, b2| b1 ^ b2 }.pack('C*')
  end
end
