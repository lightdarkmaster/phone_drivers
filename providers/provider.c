#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    int (*get_value)(void *data);
} Provider;

Provider *provider_create(const char *name, int (*get_value)(void *data)) {
    Provider *provider = malloc(sizeof(Provider));
    provider->name = strdup(name);
    provider->get_value = get_value;
    return provider;
}

void provider_free(Provider *provider) {
    free(provider->name);
    free(provider);
}

int provider_get_value(Provider *provider, void *data) {
    return provider->get_value(data);
}

const char *provider_get_name(Provider *provider) {
    return provider->name;
}
