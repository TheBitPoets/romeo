ARG PYTHON_BASE_IMAGE
FROM ${PYTHON_BASE_IMAGE}

LABEL org.opencontainers.image.title="Romeo untrusted submission runner" \
      org.opencontainers.image.source="https://github.com/TheBitPoets/romeo" \
      org.opencontainers.image.licenses="Apache-2.0" \
      io.thebitlab.runtime-id="romeo-sim" \
      io.thebitlab.worker-schemas="romeo.command_trace.v1,romeo.behavioural_result.v1"

COPY docker/runtime-runner/requirements.lock /tmp/requirements.lock
COPY docker/runtime-runner/wheelhouse /tmp/wheelhouse
COPY pyproject.toml README.md /opt/romeo/
COPY src /opt/romeo/src
RUN python -m pip install \
        --no-cache-dir \
        --no-index \
        --find-links=/tmp/wheelhouse \
        --require-hashes \
        -r /tmp/requirements.lock \
    && python -m pip install --no-cache-dir --no-deps --no-build-isolation /opt/romeo \
    && useradd --uid 65532 --create-home --shell /usr/sbin/nologin runner \
    && rm -rf /tmp/requirements.lock /tmp/wheelhouse
ENV PYTHONUTF8=1

WORKDIR /submission
USER runner
ENTRYPOINT ["python", "-I", "-m", "romeo.integrations.thebitlab.sandbox_worker"]
