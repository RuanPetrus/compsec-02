# AES e CTR
O programa é capaz de codificar, e decodificar segundo o AES. E tambem funciona 
no modo CTR

# Como usar
O programa recebe os textos por STDIN, por conveniencia 
podemos escrever os textos em um arquivo e pipar o texto com 
o comando `cat`. Podemos também rodar o programa escrever o 
input e depois finalizar com o <C-D>.

## Exemplo:
```
# exemplo_en.txt
regulating the circulation.  whenever i
find myself growing grim about the mouth; whenever it is a damp,
drizzly november in my soul; whenever i find myself involuntarily
pausing before coffin warehouses, and bringing up the rear of every
funeral i meet; and especially whenever my hypos get such an upper
hand of me, that it requires a strong moral principle to prevent me
from deliberately stepping into the street, and methodically knocking
people's hats off--then, i account it high time to get to sea as soon
as i can.  this is my substitute for pistol and ball.  with a
philosophical flourish cato throws himself upon his sword; i quietly
take to the ship.  there is nothing surprising in this.  if they but
knew it, almost all men in their degree, some time or other, cherish
very nearly the same feelings towards the ocean with me.
```
Para encryptar com o aes escolhemos a senha e a quantidade de rounds. No caso 
do exemplo a baixo a senha é 10123 e faremos a encryptação com os 10 rounds

```bash
cat example_aes.txt | python3 main.py encrypt_aes 10123 10
```
Para encryptar e decryptar com o aes
```bash
cat example_aes.txt | python3 main.py encrypt_aes 10123 10 \
					| python3 main.py decrypt_aes 10123 10
```

Para encryptar com o modo ctr e decryptar.
```bash
cat example_ctr.txt | python3 main.py encrypt_ctr 10123 10 \
					| python3 main.py decrypt_ctr 10123 10
```
