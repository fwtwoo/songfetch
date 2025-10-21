class Songfetch < Formula
  desc "A CLI tool that displays current song information in the terminal"
  homepage "https://github.com/fwtwoo/songfetch"
  url "https://github.com/fwtwoo/songfetch/archive/refs/tags/v1.0.2.tar.gz"
  sha256 "1b4c73283d7b5981b314ae3f77b6150947077aa505ab8869bb12bce0df6f7bf4"
  license "GPL-2.0"

  depends_on "python@3.14"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/songfetch", "--help"
  end
end