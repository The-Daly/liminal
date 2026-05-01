#include "LDGameModeBase.h"
#include "LDPlayerCharacter.h"

ALDGameModeBase::ALDGameModeBase()
{
    DefaultPawnClass = ALDPlayerCharacter::StaticClass();
}
