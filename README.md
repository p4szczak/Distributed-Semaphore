# Distributed-Semaphore

## Opis projektu

W ramach projektu przedstawiona została realizacja zdalnego semafora uogólnionego (zliczającego, z możliwością opuszczenia/podniesienia o wartość wskazaną jako parametr) do synchronizacji zdalnych procesów.

## Wykorzystane narzędzia

Projekt został zrealizowany przy pomocy języka __Python 3.7__ i biblioteki [RPCUDP](https://github.com/bmuller/rpcudp).
Do synchroznizacji zostały wykorzystane klasy: __Semaphore__ i __Lock__ z biblioteki [asyncio](https://docs.python.org/3/library/asyncio-sync.html).

## Opis metod

* _rpc_create(ident: int, maxState: int)_  &rarr; funkcja odpowiada za stworzenie nowego semafora o identyfikatorze _ident_ i dodania go do słownika _semaphoresDirectory_ przechowującego wszystkie powstałe semafory. Identyfikator pozwala na weryfikację, czy semafor nie został wcześniej stworzony.

* _rpc_acquire(ident: int, maxState: int)_ &rarr; funkcja odpowiada za opuszczenie semafora o podanym identyfikatorze o podaną wartość. Przed próbą opuszczenia następuje sprawdzenie, czy podany semafor istnieje, jeżeli tak zostaje zakładany zamek _semaphoreAcquireLock_ na czas opuszczania semafora o podaną wartość.

* _rpc_release(ident: int, maxState: int)_ &rarr; funkcja odpowiada za podniesienie semafora o podanym identyfikatorze o podaną wartość. Przed próbą podniesienia następuje sprawdzenie, czy podany semafor istnieje, jeżeli tak zostaje zakładany zamek _semaphoreReleaseLock_ na czas podnoszenia semafora o podaną wartość.

## Uruchamianie programu

### Uruchomienie serwera

```bash
python3 RPCServer.py
```

### Uruchomienie klienta

```bash
python3 RPCClient.py <port>
```
