use Crypt::CBC;
$cipher = Crypt::CBC->new({
key => "ExQLgXAAgvqYLjMfNCydzUNKu",
cipher => 'Blowfish',
header => 'randomiv'
});
$encrypted = $cipher->encrypt("This should be readable.");
print $cipher->decrypt($encrypted) . "\n";
