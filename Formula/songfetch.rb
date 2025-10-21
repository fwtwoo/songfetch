class Songfetch < Formula
  desc "A CLI tool that displays current song information in the terminal"
  homepage "https://github.com/fwtwoo/songfetch"
  url "https://github.com/fwtwoo/songfetch/archive/refs/tags/v1.0.2.tar.gz"
  sha256 "71ba5a2649c59caa9bfb12ceb8077857241aed25a40631d78acbe634aa28f144"
  license "GPL-2.0"

  depends_on "python@3.14"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/songfetch", "--help"
  end
end